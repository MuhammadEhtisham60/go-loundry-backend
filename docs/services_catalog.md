# Services Catalog Module

## Purpose
Manages laundry services (e.g. Wash & Fold, Dry Cleaning, Ironing), active prices, and custom sequence ordering.

---

## Models

### Service

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| name | String | Service name |
| description | String | Details of service |
| price | Decimal | Price per unit (PKR) |
| order_sequence | Integer | Placement index for sorting catalog |
| is_active | Boolean | Active status flag |
| is_deleted | Boolean | Soft deletion flag |

---

## Business Rules

- **Soft Deletion**: Services are never deleted from the database using SQL `DELETE`. Instead, they are flagged with `is_deleted = True`. This ensures old order details linked to these services do not break due to foreign key constraints.
- Soft-deleted services are omitted automatically from customer-facing selectors.
- Display sorting defaults to ascending sequence number (`order_sequence`).

---

## Endpoints

### List Catalog Services
`GET /api/services/`

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Services catalog retrieved.",
  "data": [
    {
      "id": "cb1c7e91-768a-4467-8db1-18fa1b490f23",
      "name": "Wash & Iron",
      "description": "Standard wash and machine press",
      "price": "150.00",
      "order_sequence": 1
    }
  ]
}
```

---

### Reorder Sequences
`POST /api/services/reorder/`

#### Request Payload
```json
{
  "sequences": [
    {
      "service_id": "cb1c7e91-768a-4467-8db1-18fa1b490f23",
      "order_sequence": 2
    }
  ]
}
```

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Services catalog reordered successfully.",
  "data": null
}
```
