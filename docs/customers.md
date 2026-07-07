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
`GET /api/admin/users/`

#### Query Parameters
- `role`: Filter by account role (e.g. `CUSTOMER`).
- `search`: Find by name, email, or phone.

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Users list retrieved.",
  "data": [
    {
      "id": "23a1fbc3-488f-4cb1-8cb4-bfd4b971a819",
      "email": "customer@example.com",
      "phone": "03001234567",
      "full_name": "John Doe",
      "is_blocked": false
    }
  ]
}
```

---

### Block Account
`POST /api/admin/users/{id}/block/`

#### Request Payload
None required.

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "User blocked successfully.",
  "data": {
    "id": "23a1fbc3-488f-4cb1-8cb4-bfd4b971a819",
    "is_blocked": true
  }
}
```

---

### Unblock Account
`POST /api/admin/users/{id}/unblock/`

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "User unblocked successfully.",
  "data": {
    "id": "23a1fbc3-488f-4cb1-8cb4-bfd4b971a819",
    "is_blocked": false
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
