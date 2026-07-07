# Postman Reviews Collection Guide

---

## Submit Review

### Method
`POST`

### URL
`{{BASE_URL}}/api/reviews/`

### Headers
```text
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

### Request Body
```json
{
  "order_id": "c018a1be-7443-41bb-b054-d83bebf0f9d9",
  "rating": 5,
  "remarks": "Super clean clothes!"
}
```

### Success Response (201 Created)
```json
{
  "success": true,
  "message": "Review submitted successfully.",
  "data": {
    "id": "e9e4f5a3-7e4f-4d3a-b8fb-47dbfa8f01b1",
    "order": "c018a1be-7443-41bb-b054-d83bebf0f9d9",
    "rating": 5,
    "remarks": "Super clean clothes!"
  }
}
```

### Permissions
- Customer only.
