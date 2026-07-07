# Postman Notifications Collection Guide

---

## List Notifications

### Method
`GET`

### URL
`{{BASE_URL}}/api/notifications/`

### Headers
```text
Authorization: Bearer {{access_token}}
```

### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Notification logs retrieved.",
  "data": [
    {
      "id": "23a1fbc3-488f-4cb1-8cb4-bfd4b971a819",
      "title": "Welcome to GoLaundry",
      "body": "Thanks for signing up!",
      "notification_type": "PUSH",
      "is_sent": true,
      "created_at": "2026-06-27T10:00:00Z"
    }
  ]
}
```

### Permissions
- Customer (lists own).
