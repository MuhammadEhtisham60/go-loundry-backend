# Notifications Module

## Purpose
Logs transactional SMS alerts and FCM push notifications sent to customers for delivery tracking and support updates.

---

## Models

### NotificationLog

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| user | FK(User) | Notification recipient |
| title | String | Title header of alert |
| body | Text | Alert contents |
| notification_type | Enum | `PUSH` or `SMS` |
| is_sent | Boolean | Dispatched status indicator |
| created_at | DateTime | Timestamp |

---

## Business Rules

- Every order status transition (placed, confirmed, delivered, cancelled) triggers a push notification log record automatically.
- Accounts verified with phone credentials also trigger SMS logs alongside push alerts.

---

## Endpoints

### List Notifications
`GET /api/notifications/`

#### Success Response (200 OK)
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
