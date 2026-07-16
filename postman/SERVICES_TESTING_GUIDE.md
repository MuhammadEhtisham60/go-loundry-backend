# 🧺 GoLaundry Services Catalog API Flow & Postman Testing Guide

This guide describes how to view, manage, and test the laundry services catalog using the GoLaundry Postman collection. It documents permissions, request schemas, status codes, and response structures for all catalog endpoints.

---

## 🛠️ Permissions & Access Control

The services catalog endpoints restrict mutations to Administrative users to ensure catalog pricing, items, and display sequences are not modified by unauthorized users.

| Endpoint | HTTP Method | Access Level | Description |
| :--- | :--- | :--- | :--- |
| `/api/services/` | `GET` | Public (`AllowAny`) | Lists all active services. Admins can view inactive ones by appending `?include_inactive=true`. |
| `/api/services/` | `POST` | Admin/Super Admin | Creates a new catalog service item. |
| `/api/services/<id>/` | `GET` | Public (`AllowAny`) | Retrieves a single service. Inactive services return `404` for Customers, but `200` for Admins. |
| `/api/services/<id>/` | `PUT` | Admin/Super Admin | Performs a full update of a service. |
| `/api/services/<id>/` | `PATCH` | Admin/Super Admin | Performs a partial update of a service. |
| `/api/services/<id>/` | `DELETE` | Admin/Super Admin | Soft-deletes a service from the catalog. |
| `/api/services/reorder/` | `POST` | Admin/Super Admin | Bulk reorders the catalog display sequences. |

> [!NOTE]
> All Admin mutations (POST, PUT, PATCH, DELETE, and Reorder) require an active administrative JWT token set in the `Authorization` header as `Bearer {{access_token}}`.

---

## 📋 Endpoint Reference

### 1. List Services Catalog
Retrieve all services from the catalog.

- **HTTP Method**: `GET`
- **URL**: `{{base_url}}/api/services/`
- **Query Params**:
  - `include_inactive` (optional, boolean, default `true` for Admins, ignored for Customers): Returns inactive services if `true` and requested by Admin.
- **Access**: Public
- **Handler View**: `ServiceListView`

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "Services catalog retrieved successfully.",
  "data": [
    {
      "id": "e98e4e94-c782-4f3b-a5cc-efdc5456f91f",
      "name": "Wash & Iron",
      "description": "Machine wash and press",
      "unit": "PIECE",
      "unit_display": "Per piece",
      "price": "150.00",
      "is_active": true,
      "display_order": 1,
      "created_at": "2026-07-14T06:15:40.123Z",
      "updated_at": "2026-07-14T06:15:40.123Z"
    }
  ]
}
```

---

### 2. Get Service Details
Retrieve details of a single service by ID.

- **HTTP Method**: `GET`
- **URL**: `{{base_url}}/api/services/:id/`
- **Access**: Public (Active only for Customers, Active/Inactive for Admins)
- **Handler View**: `ServiceDetailView`

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "Service details retrieved successfully.",
  "data": {
    "id": "e98e4e94-c782-4f3b-a5cc-efdc5456f91f",
    "name": "Wash & Iron",
    "description": "Machine wash and press",
    "unit": "PIECE",
    "unit_display": "Per piece",
    "price": "150.00",
    "is_active": true,
    "display_order": 1,
    "created_at": "2026-07-14T06:15:40.123Z",
    "updated_at": "2026-07-14T06:15:40.123Z"
  }
}
```

**Error Response (`404 Not Found`)** (If the service is soft-deleted, or if it is inactive and requested by a customer/anonymous user):
```json
{
  "detail": "No Service matches the given query."
}
```

---

### 3. Create Service
Add a new service to the laundry catalog.

- **HTTP Method**: `POST`
- **URL**: `{{base_url}}/api/services/`
- **Access**: Admin / Super Admin
- **Handler View**: `ServiceListView`

**Request Body**:
```json
{
  "name": "Shoe Cleaning",
  "description": "Premium sneaker and leather shoe dry clean",
  "unit": "PAIR",
  "price": 250.00,
  "is_active": true,
  "display_order": 4
}
```

**Success Response (`201 Created`)**:
```json
{
  "success": true,
  "message": "Catalog service created successfully.",
  "data": {
    "id": "d027b409-7a54-47b1-bd2e-c760a0a55255",
    "name": "Shoe Cleaning",
    "description": "Premium sneaker and leather shoe dry clean",
    "unit": "PAIR",
    "unit_display": "Per pair",
    "price": "250.00",
    "is_active": true,
    "display_order": 4,
    "created_at": "2026-07-14T11:15:37.456Z",
    "updated_at": "2026-07-14T11:15:37.456Z"
  }
}
```

---

### 4. Update Service (PUT)
Fully update an existing service item.

- **HTTP Method**: `PUT`
- **URL**: `{{base_url}}/api/services/:id/`
- **Access**: Admin / Super Admin
- **Handler View**: `ServiceDetailView`

**Request Body**:
```json
{
  "name": "Shoe Cleaning & Polish",
  "description": "Sneaker and leather shoe wash and color restoration",
  "unit": "PAIR",
  "price": 320.00,
  "is_active": true,
  "display_order": 4
}
```

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "Catalog service updated successfully.",
  "data": {
    "id": "d027b409-7a54-47b1-bd2e-c760a0a55255",
    "name": "Shoe Cleaning & Polish",
    "description": "Sneaker and leather shoe wash and color restoration",
    "unit": "PAIR",
    "unit_display": "Per pair",
    "price": "320.00",
    "is_active": true,
    "display_order": 4,
    "created_at": "2026-07-14T11:15:37.456Z",
    "updated_at": "2026-07-14T11:20:01.890Z"
  }
}
```

---

### 5. Partial Update Service (PATCH)
Modify specific fields of a service without sending the full payload.

- **HTTP Method**: `PATCH`
- **URL**: `{{base_url}}/api/services/:id/`
- **Access**: Admin / Super Admin
- **Handler View**: `ServiceDetailView`

**Request Body** (e.g. updating the price and active status only):
```json
{
  "price": 350.00,
  "is_active": false
}
```

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "Catalog service updated successfully.",
  "data": {
    "id": "d027b409-7a54-47b1-bd2e-c760a0a55255",
    "name": "Shoe Cleaning & Polish",
    "description": "Sneaker and leather shoe wash and color restoration",
    "unit": "PAIR",
    "unit_display": "Per pair",
    "price": "350.00",
    "is_active": false,
    "display_order": 4,
    "created_at": "2026-07-14T11:15:37.456Z",
    "updated_at": "2026-07-14T11:22:15.111Z"
  }
}
```

---

## 6. Delete Service
Soft-delete a service. Soft-deleted services will be hidden from all lists and details responses.

- **HTTP Method**: `DELETE`
- **URL**: `{{base_url}}/api/services/:id/`
- **Access**: Admin / Super Admin
- **Handler View**: `ServiceDetailView`

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "Catalog service deleted successfully.",
  "data": null
}
```

---

## 7. Reorder Services Catalog
Update the sequence order of multiple services simultaneously.

- **HTTP Method**: `POST`
- **URL**: `{{base_url}}/api/services/reorder/`
- **Access**: Admin / Super Admin
- **Handler View**: `ServiceReorderView`

**Request Body**:
```json
{
  "services": [
    {
      "id": "e98e4e94-c782-4f3b-a5cc-efdc5456f91f",
      "display_order": 2
    },
    {
      "id": "d027b409-7a54-47b1-bd2e-c760a0a55255",
      "display_order": 1
    }
  ]
}
```

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "Catalog service display ordering updated.",
  "data": null
}
```
