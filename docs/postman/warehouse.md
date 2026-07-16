# Postman Warehouse & Delivery Tiers API Guide

This guide details all API endpoints for managing the GoLaundry central warehouse settings and distance-based delivery tiers.

---

## 1. Retrieve Warehouse Settings

### Method
`GET`

### URL
`{{BASE_URL}}/api/locations/warehouse/`

### Headers
*None (Publicly Accessible)*

### Success Response (200 OK)
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

### Permissions
- Public access.

---

## 2. Update Warehouse Settings

### Method
`PUT`

### URL
`{{BASE_URL}}/api/locations/warehouse/`

### Headers
```text
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

### Request Body
```json
{
  "latitude": 31.5204,
  "longitude": 74.3587,
  "max_service_radius_km": 15,
  "address": "Block 7, Industrial Estate, Lahore"
}
```

### Success Response (200 OK)
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

### Permissions
- Super Admin only.

---

## 3. Retrieve Delivery Tiers

### Method
`GET`

### URL
`{{BASE_URL}}/api/locations/tiers/`

### Headers
*None (Publicly Accessible)*

### Success Response (200 OK)
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

### Permissions
- Public access.

---

## 4. Bulk Save/Replace Delivery Tiers

### Method
`PUT`

### URL
`{{BASE_URL}}/api/locations/tiers/`

### Headers
```text
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

### Request Body
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

### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Delivery tiers saved successfully.",
  "data": [
    {
      "id": 4,
      "from": 0,
      "to": 5,
      "charge": 0
    },
    {
      "id": 5,
      "from": 5,
      "to": 10,
      "charge": 100
    },
    {
      "id": 6,
      "from": 10,
      "to": 15,
      "charge": 200
    }
  ]
}
```

### Permissions
- Super Admin only.

---

## 5. Add Single Delivery Tier

### Method
`POST`

### URL
`{{BASE_URL}}/api/locations/tiers/`

### Headers
```text
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

### Request Body
```json
{
  "from": 15,
  "to": 20,
  "charge": 300
}
```

### Success Response (201 Created)
```json
{
  "success": true,
  "message": "Delivery tier created successfully.",
  "data": {
    "id": 7,
    "from": 15,
    "to": 20,
    "charge": 300
  }
}
```

### Permissions
- Super Admin only.

---

## 6. Delete Single Delivery Tier

### Method
`DELETE`

### URL
`{{BASE_URL}}/api/locations/tiers/{{tier_id}}/`

### Headers
```text
Authorization: Bearer {{access_token}}
```

### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Delivery tier deleted successfully.",
  "data": null
}
```

### Permissions
- Super Admin only.

---

## 7. Validate Client Area eligibility & Charges

### Method
`POST`

### URL
`{{BASE_URL}}/api/locations/validate-area/`

### Headers
```text
Content-Type: application/json
```

### Request Body
```json
{
  "latitude": 31.4697,
  "longitude": 74.4112
}
```

### Success Response (Inside operational boundary) (200 OK)
```json
{
  "success": true,
  "message": "Location checked successfully.",
  "data": {
    "is_valid": true,
    "distance_km": 4.23,
    "delivery_charge": 0.00,
    "warehouse_latitude": "31.520400",
    "warehouse_longitude": "74.358700",
    "warehouse_address": "Block 7, Industrial Estate, Lahore",
    "max_service_radius_km": "15.00"
  }
}
```

### Success Response (Outside boundary) (200 OK)
```json
{
  "success": true,
  "message": "Location checked successfully.",
  "data": {
    "is_valid": false,
    "distance_km": 18.45,
    "delivery_charge": 0.00,
    "warehouse_latitude": "31.520400",
    "warehouse_longitude": "74.358700",
    "warehouse_address": "Block 7, Industrial Estate, Lahore",
    "max_service_radius_km": "15.00"
  }
}
```

### Permissions
- Public access.
