# Postman Locations & Warehouse Guide

---

## Validate Service Area

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
  "latitude": 24.8050,
  "longitude": 67.0250
}
```

### Success Response (200 OK)
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

### Permissions
- Public Access.
