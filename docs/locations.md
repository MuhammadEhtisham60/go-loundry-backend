# Locations & Warehouse Module

## Purpose
Enforces the geographical service area limits and calculates delivery fees dynamically using distance-based tiers.

---

## Models

### WarehouseSetting

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| latitude | Decimal | Warehouse coordinate |
| longitude | Decimal | Warehouse coordinate |
| max_service_radius_km | Decimal | Operational boundary limit (e.g. 10.00 km) |

### DeliveryTier

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| min_distance_km | Decimal | Lower bound distance (inclusive) |
| max_distance_km | Decimal | Upper bound distance (exclusive) |
| charge | Decimal | Delivery fee in PKR |

---

## Business Rules

- Estimates the straight-line distance from the warehouse coordinates to the customer's coordinates using the **Haversine formula**.
- An address coordinate is only serviced if the calculated distance is less than or equal to `WarehouseSetting.max_service_radius_km`.
- Shipping fees are matched dynamically from the `DeliveryTier` bands. If a tier matches the distance, its `charge` is applied. If no tier is configured for a valid distance, the delivery charge defaults to **Rs.0**.

---

## Endpoints

### Validate Service Area & Charges
`POST /api/locations/validate-area/`

#### Request Payload
```json
{
  "latitude": 24.8050,
  "longitude": 67.0250
}
```

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Service area validated.",
  "data": {
    "is_valid": true,
    "distance_km": 1.48,
    "delivery_charge": 50.00
  }
}
```

#### Success Response (Out of Range - 200 OK)
```json
{
  "success": true,
  "message": "Service area validated.",
  "data": {
    "is_valid": false,
    "distance_km": 12.35,
    "delivery_charge": 0.00
  }
}
```
