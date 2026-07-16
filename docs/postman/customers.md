# Postman Customer Management Guide

---

## List Customers

### Method
`GET`

### URL
`{{BASE_URL}}/api/users/`

### Headers
```text
Authorization: Bearer {{access_token}}
```

### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Customer records list retrieved.",
  "data": [
    {
      "id": "e98e4e94-c782-4f3b-a5cc-efdc5456f91f",
      "email": "customer@example.com",
      "phone": "03001234567",
      "full_name": "John Doe",
      "profile_photo": null,
      "is_blocked": false,
      "created_at": "2026-07-16T10:00:00Z"
    }
  ]
}
```

### Permissions
- Support Agent, Admin, Super Admin only.

---

## Block/Unblock Account

### Method
`POST`

### URL
`{{BASE_URL}}/api/users/e98e4e94-c782-4f3b-a5cc-efdc5456f91f/block/`

### Headers
```text
Authorization: Bearer {{access_token}}
```

### Request Body
```json
{
  "is_blocked": true
}
```

### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Customer account blocked successfully.",
  "data": {
    "id": "e98e4e94-c782-4f3b-a5cc-efdc5456f91f",
    "email": "customer@example.com",
    "phone": "03001234567",
    "full_name": "John Doe",
    "profile_photo": null,
    "is_blocked": true,
    "created_at": "2026-07-16T10:00:00Z"
  }
}
```

### Permissions
- Admin and Super Admin only.

