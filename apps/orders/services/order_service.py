from decimal import Decimal
from typing import Dict, Any, List
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.orders.models import Order, OrderItem, OrderStatus
from apps.addresses.models import Address
from apps.services_catalog.models import Service
from apps.locations.services import LocationService
from apps.common.services.notifications import NotificationService

User = get_user_model()


class OrderService:
    """
    Service layer implementing all order creation, cancellation, status updates,
    and automatic calculations (distance validation, delivery charge mapping, etc.).
    """

    @staticmethod
    def create_order(user: User, validated_data: Dict[str, Any]) -> Order:
        """
        Validates the delivery coverage area, calculates pricing tiers, and
        saves the Order and OrderItem records in a transaction block.
        """
        address_id = validated_data["pickup_address_id"]
        pickup_date = validated_data["pickup_date"]
        pickup_slot = validated_data["pickup_slot"]
        special_instructions = validated_data.get("special_instructions", "")
        items_data = validated_data["items"]

        # 1. Fetch and validate address
        address = get_object_or_404(Address, id=address_id, user=user)

        # 2. Check service area
        area_check = LocationService.validate_service_area(
            float(address.latitude), float(address.longitude)
        )
        if not area_check["is_valid"]:
            raise serializers.ValidationError(
                "We are not in your area yet! Coming soon to your neighbourhood"
            )

        distance_km = area_check["distance_km"]
        delivery_charge = area_check["delivery_charge"]

        with transaction.atomic():
            # 3. Create the base Order record first (using temp total amounts)
            order = Order.objects.create(
                user=user,
                pickup_address=address,
                address_line_snapshot=address.address_line,
                latitude=address.latitude,
                longitude=address.longitude,
                distance_km=Decimal(str(distance_km)),
                delivery_charge=delivery_charge,
                total_services_amount=Decimal("0.00"),
                total_amount=Decimal("0.00"),
                pickup_date=pickup_date,
                pickup_slot=pickup_slot,
                special_instructions=special_instructions,
            )

            # 4. Create items and sum service values
            total_services = Decimal("0.00")
            for item in items_data:
                service = get_object_or_404(
                    Service, id=item["service_id"], is_active=True
                )
                qty = Decimal(str(item["quantity"]))
                total_price = qty * service.price

                OrderItem.objects.create(
                    order=order,
                    service=service,
                    quantity=qty,
                    unit_price=service.price,
                    total_price=total_price,
                )
                total_services += total_price

            # 5. Save calculated sums to order
            order.total_services_amount = total_services
            order.total_amount = total_services + delivery_charge
            order.save()

        # 6. Trigger notifications
        NotificationService.send_push(
            user.id,
            "Order Placed",
            f"Your order #{order.id} has been placed successfully.",
        )
        if user.phone:
            NotificationService.send_sms(
                user.phone,
                f"Your GoLaundry order #{order.id} has been placed. We will pick up in the {pickup_slot}.",
            )

        return order

    @staticmethod
    def cancel_order(user: User, order_id: str, reason: str) -> Order:
        """
        Cancels an order. Customers can only cancel if status is ORDER_PLACED.
        Administrators can cancel at any stage.
        """
        is_admin = user.role in ["ADMIN", "SUPER_ADMIN"]
        order = get_object_or_404(Order, id=order_id)

        if not is_admin and order.user != user:
            raise serializers.ValidationError("Unauthorized.")

        if not is_admin and order.status != OrderStatus.ORDER_PLACED:
            raise serializers.ValidationError(
                "Orders can only be cancelled before they are confirmed."
            )

        order.status = OrderStatus.CANCELLED
        order.cancellation_reason = reason
        order.save()

        # Trigger notifications
        NotificationService.send_push(
            order.user.id,
            "Order Cancelled",
            f"Your order #{order.id} was cancelled.",
        )
        if order.user.phone:
            NotificationService.send_sms(
                order.user.phone,
                f"Your GoLaundry order #{order.id} has been cancelled.",
            )

        return order

    @staticmethod
    def update_order_status(
        order_id: str, status_value: str, extra_data: Dict[str, Any]
    ) -> Order:
        """
        Updates an order status and records notes / rider details.
        Only accessible by Admin/Support Agent roles.
        """
        order = get_object_or_404(Order, id=order_id)
        order.status = status_value

        # Optional updates
        if "rider_name" in extra_data:
            order.rider_name = extra_data["rider_name"]
        if "rider_contact" in extra_data:
            order.rider_contact = extra_data["rider_contact"]
        if "admin_notes" in extra_data:
            order.admin_notes = extra_data["admin_notes"]

        order.save()

        # Trigger notifications based on status change
        msg = f"Your order status has been updated to {order.get_status_display()}."
        NotificationService.send_push(order.user.id, "Order Update", msg)

        # SMS trigger on key status milestones
        if status_value in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
            if order.user.phone:
                NotificationService.send_sms(order.user.phone, msg)

        return order

    @staticmethod
    def reorder(
        user: User, order_id: str, pickup_date: Any, pickup_slot: str
    ) -> Order:
        """
        Pre-fills details of a previous order and clones it into a new active checkout.
        """
        old_order = get_object_or_404(Order, id=order_id, user=user)

        # Extract items
        items_payload = []
        for item in old_order.items.all():
            items_payload.append(
                {"service_id": str(item.service_id), "quantity": float(item.quantity)}
            )

        new_order_payload = {
            "pickup_address_id": str(old_order.pickup_address_id),
            "pickup_date": pickup_date,
            "pickup_slot": pickup_slot,
            "special_instructions": old_order.special_instructions,
            "items": items_payload,
        }

        return OrderService.create_order(user, new_order_payload)
