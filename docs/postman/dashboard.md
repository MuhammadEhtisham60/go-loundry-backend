# Postman Dashboard Collection Guide

---

## Get Dashboard Stats

### Method
`GET`

### URL
`{{BASE_URL}}/api/admin/dashboard/stats/`

### Headers
```text
Authorization: Bearer {{access_token}}
```

### Success Response (200 OK)
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

### Permissions
- Support Agent, Admin, Super Admin.
