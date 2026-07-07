# Support Chats Module

## Purpose
Enables real-time communication between customers and back-office support agents for order queries and assistance.

---

## Models

### Conversation

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| customer | FK(User) | Customer participant |
| assigned_agent | FK(User) | Support agent handler |
| is_resolved | Boolean | Resolution state indicator |

### Message

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| conversation | FK(Conversation) | Chat thread |
| sender | FK(User) | Message author |
| text | Text | Message body |
| image_url | URL | Uploaded attachment path |

---

## Business Rules

- A Customer can have at most **one** active (unresolved) conversation session open. Starting a conversation retrieves this active chat or constructs a new one.
- **Auto Re-opening**: If a Customer posts a message to a conversation that was previously marked `is_resolved = True`, the system automatically resets `is_resolved` to `False` to notify the support desk.
- Support agents can assign threads to themselves and toggle the resolution status.

---

## Endpoints

### Start Conversation
`POST /api/chats/conversations/`

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Support session initialized.",
  "data": {
    "id": "e9e4f5a3-7e4f-4d3a-b8fb-47dbfa8f01b1",
    "customer": {
      "email": "customer@example.com"
    },
    "assigned_agent": null,
    "is_resolved": false
  }
}
```

---

### Send Message (Text / Image Attachment)
`POST /api/chats/conversations/{id}/messages/`

- **Content-Type**: `multipart/form-data` if uploading attachments.

#### Request Parameters
- `text`: Text message.
- `image`: Binary file (optional).

#### Success Response (201 Created)
```json
{
  "success": true,
  "message": "Message sent successfully.",
  "data": {
    "id": "848a3e94-c782-4f3b-a5cc-efdc5456f91f",
    "text": "Please check my delivery status.",
    "image_url": "https://storage.googleapis.com/go-laundry-media/chats/attachment.jpg"
  }
}
```
