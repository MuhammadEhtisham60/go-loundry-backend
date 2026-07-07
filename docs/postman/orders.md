# Postman Orders Collection Guide

---

## Place Order

### Method
`POST`

### URL
`{{BASE_URL}}/api/orders/`

### Headers
```text
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

### Request Body
```json
{
  "pickup_address_id": "7fa5701a-85d7-4638-9584-18fa1b490f23",
  "pickup_date": "2026-06-28",
  "pickup_slot": "MORNING",
  "special_instructions": "Dry clean red dress",
  "items": [
    {
      "service_id": "cb1c7e91-768a-4467-8db1-18fa1b490f23",
      "quantity": 2.0
    }
  ]
}
```

### Success Response (201 Created)
```json
{
  "success": true,
  "message": "Order placed successfully.",
  "data": {
    "id": "c018a1be-7443-41bb-b054-d83bebf0f9d9",
    "status": "ORDER_PLACED",
    "delivery_charge": "50.00",
    "total_amount": "350.00"
  }
}
```

### Validation Errors (400 Bad Request - Out of coverage)
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": [
    "We are not in your area yet! Coming soon to your neighbourhood"
  ]
}
```

### Permissions
- Customer only.
