import datetime
from typing import Dict, Any
from django.utils import timezone
from django.db.models import Sum, Count, Q
from apps.orders.models import Order, OrderStatus
from apps.authentication.models.user import User, UserRole, UserType
from apps.chats.models import Conversation


class DashboardSelector:
    """
    Selector encapsulating read operations for compiler stats.
    Calculates dynamic metrics for the administrative overview.
    """

    @staticmethod
    def get_dashboard_stats() -> Dict[str, Any]:
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - datetime.timedelta(days=now.weekday())
        month_start = today_start.replace(day=1)

        # 1. Order Volume Totals
        total_orders_today = Order.objects.filter(created_at__gte=today_start).count()
        total_orders_week = Order.objects.filter(created_at__gte=week_start).count()
        total_orders_month = Order.objects.filter(created_at__gte=month_start).count()

        # 2. Orders grouped by status
        status_counts_raw = Order.objects.values("status").annotate(count=Count("id"))
        status_counts = {item["status"]: item["count"] for item in status_counts_raw}
        # Pre-fill standard ones to avoid missing keys on frontend
        for s in OrderStatus.values:
            status_counts.setdefault(s, 0)

        # 3. New Registrations
        new_customers_today = User.objects.filter(
            Q(role__isnull=True) | Q(user_type=UserType.USER),
            created_at__gte=today_start
        ).exclude(
            role__name__in=["Support Agent", "Admin", "Super Admin"]
        ).count()
        new_customers_week = User.objects.filter(
            Q(role__isnull=True) | Q(user_type=UserType.USER),
            created_at__gte=week_start
        ).exclude(
            role__name__in=["Support Agent", "Admin", "Super Admin"]
        ).count()
        new_customers_month = User.objects.filter(
            Q(role__isnull=True) | Q(user_type=UserType.USER),
            created_at__gte=month_start
        ).exclude(
            role__name__in=["Support Agent", "Admin", "Super Admin"]
        ).count()


        # 4. Active Support tickets
        open_chats = Conversation.objects.filter(is_resolved=False).count()

        # 5. Total Revenue from Delivered Orders
        revenue_data = Order.objects.filter(status=OrderStatus.DELIVERED).aggregate(
            revenue=Sum("total_amount")
        )
        total_revenue = revenue_data["revenue"] or 0.00

        return {
            "order_volumes": {
                "today": total_orders_today,
                "this_week": total_orders_week,
                "this_month": total_orders_month,
            },
            "orders_by_status": status_counts,
            "new_customers": {
                "today": new_customers_today,
                "this_week": new_customers_week,
                "this_month": new_customers_month,
            },
            "open_support_chats": open_chats,
            "total_delivered_revenue": float(total_revenue),
        }
