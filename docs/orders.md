# Orders Module

## Purpose
Handles order placement, distance validation, delivery tier fee assignment, laundry status progression, rider assignments, cancellations, and reordering.

---

## Models

### Order

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| user | FK(User) | Customer placing order |
| status | Enum | Order status choices |
| pickup_address | FK(Address) | Pickup address selection |
| address_line_snapshot | String | Text snapshot of address at placement |
| latitude | Decimal | Snapshot coordinate |
| longitude | Decimal | Snapshot coordinate |
| distance_km | Decimal | Calculated distance from warehouse |
| delivery_charge | Decimal | Applied delivery fee |
| total_services_amount | Decimal | Sum of service item costs |
| total_amount | Decimal | Grand total (services + delivery) |
| pickup_date | Date | Scheduled pickup day |
| pickup_slot | Enum | Pickup slot time band |
| payment_method | Enum | Payment method (`COD` only in Phase 1) |

---

## Business Rules

- **Coverage Bounds**: If coordinates fall outside the warehouse service radius, checkout fails with a `ValidationError`.
- **Payment Constraint**: Cash on Delivery (COD) is the only supported payment method.
- **Cancellations**: Customers can cancel an order only while it is in the `ORDER_PLACED` state. Once the status advances (e.g. `ORDER_CONFIRMED` or rider assigned), cancellations are blocked for customers. Admins can cancel at any stage.
- **Reordering**: Takes the services and quantities from a previous order and pre-fills them as a new active checkout payload with a new slot date.

---

## Endpoints

### Place Order
`POST /api/orders/`

#### Request Payload
```json
{
  "pickup_address_id": "7fa5701a-85d7-4638-9584-18fa1b490f23",
  "pickup_date": "2026-06-28",
  "pickup_slot": "MORNING",
  "special_instructions": "Please hang shirts",
  "items": [
    {
      "service_id": "cb1c7e91-768a-4467-8db1-18fa1b490f23",
      "quantity": 2.0
    }
  ]
}
```

#### Success Response (201 Created)
```json
{
  "success": true,
  "message": "Order placed successfully.",
  "data": {
    "id": "c018a1be-7443-41bb-b054-d83bebf0f9d9",
    "status": "ORDER_PLACED",
    "distance_km": "1.48",
    "delivery_charge": "50.00",
    "total_services_amount": "300.00",
    "total_amount": "350.00",
    "pickup_date": "2026-06-28",
    "pickup_slot": "MORNING"
  }
}
```

---

### Update Status (Admin/Support Only)
`PUT /api/orders/{id}/status/`

#### Request Payload
```json
{
  "status": "PICKUP_ASSIGNED",
  "rider_name": "Asif Khan",
  "rider_contact": "03112345678",
  "admin_notes": "Rider dispatched"
}
```

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Order status updated successfully.",
  "data": {
    "id": "c018a1be-7443-41bb-b054-d83bebf0f9d9",
    "status": "PICKUP_ASSIGNED",
    "rider_name": "Asif Khan"
  }
}
```
