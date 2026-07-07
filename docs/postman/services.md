# Postman Services Catalog Guide

---

## List Active Services

### Method
`GET`

### URL
`{{BASE_URL}}/api/services/`

### Headers
None required.

### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Services catalog retrieved.",
  "data": [
    {
      "id": "cb1c7e91-768a-4467-8db1-18fa1b490f23",
      "name": "Wash & Iron",
      "price": "150.00",
      "order_sequence": 1
    }
  ]
}
```

### Permissions
- Public Access.
