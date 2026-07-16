from typing import Dict, Any, List
from django.db.models import Sum, Count, Avg, Case, When, Value, CharField, Q
from django.utils.dateparse import parse_date

from apps.orders.models import Order, OrderItem, OrderStatus
from apps.authentication.models.user import User, UserRole, UserType


class ReportsSelector:
    """
    Selectors for generating exportable reports and advanced analytics.
    Utilizes SQL conditional aggregates to optimize performance.
    """

    @staticmethod
    def get_orders_report(date_from: str, date_to: str) -> Dict[str, Any]:
        queryset = Order.objects.filter(created_at__date__range=[date_from, date_to])

        total_orders = queryset.count()
        status_breakdown = queryset.values("status").annotate(count=Count("id"))
        status_map = {item["status"]: item["count"] for item in status_breakdown}

        return {
            "date_range": {"from": date_from, "to": date_to},
            "total_orders": total_orders,
            "status_breakdown": status_map,
        }

    @staticmethod
    def get_revenue_report(date_from: str, date_to: str) -> Dict[str, Any]:
        # Filter only completed (delivered) orders for real revenue calculation
        queryset = Order.objects.filter(
            status=OrderStatus.DELIVERED,
            created_at__date__range=[date_from, date_to],
        )

        aggregates = queryset.aggregate(
            total_rev=Sum("total_amount"),
            avg_val=Avg("total_amount"),
            total_shipping=Sum("delivery_charge"),
            order_count=Count("id"),
        )

        return {
            "date_range": {"from": date_from, "to": date_to},
            "completed_orders_count": aggregates["order_count"] or 0,
            "total_revenue": float(aggregates["total_rev"] or 0.00),
            "average_order_value": float(aggregates["avg_val"] or 0.00),
            "total_delivery_charges": float(aggregates["total_shipping"] or 0.00),
        }

    @staticmethod
    def get_customer_report() -> Dict[str, Any]:
        queryset = User.objects.filter(
            Q(role=UserRole.CUSTOMER) | Q(user_type=UserType.USER)
        ).exclude(
            role__in=[UserRole.SUPPORT_AGENT, UserRole.ADMIN, UserRole.SUPER_ADMIN]
        )


        total_customers = queryset.count()
        blocked_count = queryset.filter(is_blocked=True).count()
        active_count = queryset.filter(is_blocked=False, is_active=True).count()

        return {
            "total_registered_customers": total_customers,
            "active_customers": active_count,
            "blocked_customers": blocked_count,
        }

    @staticmethod
    def get_service_popularity_report() -> List[Dict[str, Any]]:
        # Aggregate quantities and revenues per service name
        items_summary = (
            OrderItem.objects.values("service__name")
            .annotate(
                total_ordered_quantity=Sum("quantity"),
                total_sales_amount=Sum("total_price"),
                order_count=Count("order", distinct=True),
            )
            .order_by("-total_ordered_quantity")
        )

        return [
            {
                "service_name": item["service__name"],
                "total_quantity": float(item["total_ordered_quantity"]),
                "total_sales": float(item["total_sales_amount"]),
                "total_orders": item["order_count"],
            }
            for item in items_summary
            if item["service__name"] is not None
        ]

    @staticmethod
    def get_zone_report() -> List[Dict[str, Any]]:
        # Classify orders by Haversine distance bands and count frequencies
        zones_summary = (
            Order.objects.annotate(
                zone=Case(
                    When(distance_km__lte=5, then=Value("0 - 5 KM")),
                    When(distance_km__lte=10, then=Value("5 - 10 KM")),
                    When(distance_km__lte=15, then=Value("10 - 15 KM")),
                    default=Value("> 15 KM"),
                    output_field=CharField(),
                )
            )
            .values("zone")
            .annotate(order_count=Count("id"), revenue=Sum("total_amount"))
            .order_by("zone")
        )

        return [
            {
                "zone_band": item["zone"],
                "total_orders": item["order_count"],
                "estimated_revenue": float(item["revenue"] or 0.00),
            }
            for item in zones_summary
        ]
