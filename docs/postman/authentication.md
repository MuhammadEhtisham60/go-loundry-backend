# Postman Authentication Collection Guide

This guide maps variables and sample outputs for testing the Authentication endpoints.

---

## Register User

### Method
`POST`

### URL
`{{BASE_URL}}/api/auth/register/`

### Headers
```text
Content-Type: application/json
```

### Request Body
```json
{
  "email": "customer@example.com",
  "phone": "03001234567",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!",
  "full_name": "John Doe"
}
```

### Success Response (201 Created)
```json
{
  "success": true,
  "message": "User registered successfully.",
  "data": {
    "id": "e98e4e94-c782-4f3b-a5cc-efdc5456f91f",
    "email": "customer@example.com",
    "phone": "03001234567",
    "full_name": "John Doe",
    "role": "CUSTOMER"
  }
}
```

### Validation Errors (400 Bad Request)
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "phone": ["This field must contain a valid Pakistani mobile number starting with 03."]
  }
}
```

### Permissions
- Public Access
