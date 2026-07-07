# Postman Reports Collection Guide

---

## Get Geographical Zone Report

### Method
`GET`

### URL
`{{BASE_URL}}/api/admin/reports/zones/`

### Headers
```text
Authorization: Bearer {{access_token}}
```

### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Geographical zone report compiled.",
  "data": [
    {
      "zone_band": "0 - 5 KM",
      "total_orders": 15,
      "estimated_revenue": 3400.00
    }
  ]
}
```

### Permissions
- Admin, Super Admin.
