# Customers Module

## Purpose
Allows administrative roles to view, search, block, and unblock customer accounts.

## Why This Module Exists
It isolates sensitive customer management workflows and block flags to prevent unauthorized accounts activity.

---

## Business Rules

- Only Support Agent, Admin, and Super Admin roles can access customer profile list lookups.
- Only Admin and Super Admin roles can block or unblock accounts.
- Blocking an account immediately rejects subsequent JWT login attempts and invalidates current requests.

---

## Endpoints

### List Customers
`GET /api/users/`

#### Query Parameters
- `search`: Find by name, email, or phone.

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Customer records list retrieved.",
  "data": [
    {
      "id": "23a1fbc3-488f-4cb1-8cb4-bfd4b971a819",
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

---

### Block Account
`POST /api/users/{id}/block/`

#### Request Payload
```json
{
  "is_blocked": true
}
```

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Customer account blocked successfully.",
  "data": {
    "id": "23a1fbc3-488f-4cb1-8cb4-bfd4b971a819",
    "email": "customer@example.com",
    "phone": "03001234567",
    "full_name": "John Doe",
    "profile_photo": null,
    "is_blocked": true,
    "created_at": "2026-07-16T10:00:00Z"
  }
}
```

---

### Unblock Account
`POST /api/users/{id}/block/` (using payload `{"is_blocked": false}`)


#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Customer account unblocked successfully.",
  "data": {
    "id": "23a1fbc3-488f-4cb1-8cb4-bfd4b971a819",
    "email": "customer@example.com",
    "phone": "03001234567",
    "full_name": "John Doe",
    "profile_photo": null,
    "is_blocked": false,
    "created_at": "2026-07-16T10:00:00Z"
  }
}
```

#### Error Response (403 Forbidden - Customer attempting to block)
```json
{
  "success": false,
  "message": "You do not have permission to perform this action.",
  "errors": null
}
```
