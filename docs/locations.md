# Locations & Warehouse Module

## Purpose
Enforces the geographical service area limits and calculates delivery fees dynamically using distance-based tiers.

---

## Models

### WarehouseSetting

| Field | Type | Description |
|---|---|---|
| id | BigInt | Primary key |
| latitude | Decimal | Warehouse coordinate |
| longitude | Decimal | Warehouse coordinate |
| max_service_radius_km | Decimal | Operational boundary limit (e.g. 15.00 km) |
| address | String | Warehouse street address |

### DeliveryTier

| Field | Type | Description |
|---|---|---|
| id | BigInt | Primary key |
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

### Get Warehouse Settings
`GET /api/locations/warehouse/`

Retrieves the singleton warehouse coordinates, max radius, and address. Publicly accessible.

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Warehouse settings retrieved.",
  "data": {
    "id": 1,
    "latitude": "31.520400",
    "longitude": "74.358700",
    "max_service_radius_km": "15.00",
    "address": "Block 7, Industrial Estate, Lahore"
  }
}
```

### Update Warehouse Settings
`PUT /api/locations/warehouse/`

Updates the singleton warehouse configuration. Requires Super Admin privileges.

#### Request Payload
```json
{
  "latitude": 31.5204,
  "longitude": 74.3587,
  "max_service_radius_km": 15,
  "address": "Block 7, Industrial Estate, Lahore"
}
```

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Warehouse settings updated successfully.",
  "data": {
    "id": 1,
    "latitude": "31.520400",
    "longitude": "74.358700",
    "max_service_radius_km": "15.00",
    "address": "Block 7, Industrial Estate, Lahore"
  }
}
```

### Get Delivery Tiers
`GET /api/locations/tiers/`

Lists all configured delivery charge tiers, ordered by distance bounds. Publicly accessible. Keys are mapped dynamically to `from` and `to` for frontend ease-of-use.

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Delivery tiers list retrieved.",
  "data": [
    {
      "id": 1,
      "from": 0,
      "to": 5,
      "charge": 0
    },
    {
      "id": 2,
      "from": 5,
      "to": 10,
      "charge": 100
    }
  ]
}
```

### Bulk Save Delivery Tiers
`PUT /api/locations/tiers/`

Atomically overwrites the entire delivery tiers list with the request body array. Requires Super Admin privileges.

#### Request Payload
```json
[
  {
    "from": 0,
    "to": 5,
    "charge": 0
  },
  {
    "from": 5,
    "to": 10,
    "charge": 100
  },
  {
    "from": 10,
    "to": 15,
    "charge": 200
  }
]
```

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Delivery tiers saved successfully.",
  "data": [
    {
      "id": 1,
      "from": 0,
      "to": 5,
      "charge": 0
    },
    {
      "id": 2,
      "from": 5,
      "to": 10,
      "charge": 100
    },
    {
      "id": 3,
      "from": 10,
      "to": 15,
      "charge": 200
    }
  ]
}
```

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
  "message": "Location checked successfully.",
  "data": {
    "is_valid": true,
    "distance_km": 1.48,
    "delivery_charge": 0.00,
    "warehouse_latitude": "24.813800",
    "warehouse_longitude": "67.033600",
    "warehouse_address": "Lahore Central Warehouse",
    "max_service_radius_km": "15.00"
  }
}
```
