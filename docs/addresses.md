# Addresses Module

## Purpose
Manages multi-address profiles for customer pickups, including coordinate settings and default flag rotation rules.

---

## Models

### Address

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| user | FK(User) | Account owner |
| address_type | Enum | `HOME`, `OFFICE`, `OTHER` |
| address_line | String | Physical address description |
| latitude | Decimal | Map coordinate |
| longitude | Decimal | Map coordinate |
| is_default | Boolean | Indicates if this is the default selection |

---

## Business Rules

- A customer can configure multiple addresses.
- At most **one** address can be designated as the default at any time.
- If a new address is created or updated with `is_default = True`, any existing default address is rotated to `False`.
- If the default address is deleted, the most recently added remaining address is updated to become the new default.

---

## Endpoints

### List Addresses
`GET /api/addresses/`

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Addresses retrieved successfully.",
  "data": [
    {
      "id": "7fa5701a-85d7-4638-9584-18fa1b490f23",
      "address_type": "HOME",
      "address_line": "Suite 14, Block 5, Clifton, Karachi",
      "latitude": "24.810500",
      "longitude": "67.031000",
      "is_default": true
    }
  ]
}
```

---

### Create Address
`POST /api/addresses/`

#### Request Payload
```json
{
  "address_type": "OFFICE",
  "address_line": "Gulshan, Karachi",
  "latitude": 24.9180,
  "longitude": 67.0970,
  "is_default": false
}
```

#### Success Response (201 Created)
```json
{
  "success": true,
  "message": "Address created successfully.",
  "data": {
    "id": "e98e4e94-c782-4f3b-a5cc-efdc5456f91f",
    "address_type": "OFFICE",
    "address_line": "Gulshan, Karachi",
    "latitude": "24.918000",
    "longitude": "67.097000",
    "is_default": false
  }
}
```
