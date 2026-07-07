# Dashboard Stats Module

## Purpose
Provides high-level aggregates, operational volumes, and support tickets backlog statistics for back-office administrators.

---

## Business Rules

- Access restricted exclusively to `SUPPORT_AGENT`, `ADMIN`, and `SUPER_ADMIN` roles.
- Customer roles are rejected with a `403 Forbidden` response.
- Compiles counts for orders placed today, active support tickets, and total completed COD revenue.

---

## Endpoints

### Get Dashboard Statistics
`GET /api/admin/dashboard/stats/`

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Dashboard statistics compiled.",
  "data": {
    "order_volumes": {
      "today": 1,
      "this_week": 5,
      "this_month": 22
    },
    "orders_by_status": {
      "ORDER_PLACED": 2,
      "ORDER_CONFIRMED": 1,
      "DELIVERED": 15,
      "CANCELLED": 4
    },
    "new_customers": {
      "today": 3,
      "this_week": 14,
      "this_month": 45
    },
    "open_support_chats": 2,
    "total_delivered_revenue": 14850.00
  }
}
```

#### Error Response (403 Forbidden - Customer attempt)
```json
{
  "success": false,
  "message": "You do not have permission to perform this action.",
  "errors": null
}
```
