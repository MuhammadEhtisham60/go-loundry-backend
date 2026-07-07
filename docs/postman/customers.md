# Postman Customer Management Guide

---

## List Customers

### Method
`GET`

### URL
`{{BASE_URL}}/api/admin/users/?role=CUSTOMER`

### Headers
```text
Authorization: Bearer {{access_token}}
```

### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Users list retrieved.",
  "data": [
    {
      "id": "e98e4e94-c782-4f3b-a5cc-efdc5456f91f",
      "email": "customer@example.com",
      "phone": "03001234567",
      "full_name": "John Doe",
      "role": "CUSTOMER",
      "is_blocked": false
    }
  ]
}
```

### Permissions
- Support Agent, Admin, Super Admin only.

---

## Block Account

### Method
`POST`

### URL
`{{BASE_URL}}/api/admin/users/e98e4e94-c782-4f3b-a5cc-efdc5456f91f/block/`

### Headers
```text
Authorization: Bearer {{access_token}}
```

### Success Response (200 OK)
```json
{
  "success": true,
  "message": "User blocked successfully.",
  "data": {
    "id": "e98e4e94-c782-4f3b-a5cc-efdc5456f91f",
    "is_blocked": true
  }
}
```

### Permissions
- Admin and Super Admin only.
