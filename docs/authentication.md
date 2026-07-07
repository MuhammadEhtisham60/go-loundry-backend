# Authentication Module

## Purpose
This module handles all user registrations, credential authentication (email or phone login), OTP code lifecycles, and JWT token management.

## Why This Module Exists
It isolates sensitive credentials handling, hashing, and token generation from operational models.

---

## Models

### User

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| email | String (Unique) | User email address (optional if phone set) |
| phone | String (Unique) | User phone number (optional if email set) |
| full_name | String | User full name |
| role | Enum | User role (`CUSTOMER`, `SUPPORT_AGENT`, `ADMIN`, `SUPER_ADMIN`) |
| is_blocked | Boolean | Indicates if account is blocked |
| profile_photo | URL | User avatar link |

---

## Business Rules

- Users can register or log in using either their Email or Phone number (OTP).
- Support Agents, Admins, and Super Admins are created via admin commands or back-office interfaces.
- Users that are marked `is_blocked = True` cannot obtain JWT tokens.

---

## Endpoints

### Register User
`POST /api/auth/register/`

#### Request Payload
```json
{
  "email": "customer@example.com",
  "phone": "03001234567",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!",
  "full_name": "John Doe"
}
```

#### Success Response (201 Created)
```json
{
  "success": true,
  "message": "User registered successfully.",
  "data": {
    "id": "23a1fbc3-488f-4cb1-8cb4-bfd4b971a819",
    "email": "customer@example.com",
    "phone": "03001234567",
    "full_name": "John Doe",
    "role": "CUSTOMER"
  }
}
```

#### Error Response (400 Validation Error)
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "email": ["user with this email already exists."]
  }
}
```

---

### Login (Password)
`POST /api/auth/login/`

#### Request Payload
```json
{
  "email": "customer@example.com",
  "password": "SecurePassword123!"
}
```

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "tokens": {
      "access": "eyJhbGciOi...",
      "refresh": "eyJhbGciOi..."
    },
    "user": {
      "id": "23a1fbc3",
      "email": "customer@example.com"
    }
  }
}
```

#### Error Response (401 Unauthorized / Blocked)
```json
{
  "success": false,
  "message": "This account is blocked.",
  "errors": null
}
```
