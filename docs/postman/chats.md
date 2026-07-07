# Postman Chats Collection Guide

---

## Send Message

### Method
`POST`

### URL
`{{BASE_URL}}/api/chats/conversations/e9e4f5a3-7e4f-4d3a-b8fb-47dbfa8f01b1/messages/`

### Headers
```text
Authorization: Bearer {{access_token}}
```

### Request Body (form-data)
- `text`: "Please check my order status."
- `image`: [File Upload] (optional)

### Success Response (201 Created)
```json
{
  "success": true,
  "message": "Message sent successfully.",
  "data": {
    "id": "848a3e94-c782-4f3b-a5cc-efdc5456f91f",
    "text": "Please check my order status.",
    "image_url": null
  }
}
```

### Permissions
- Customer (for own threads), Support Agent, Admin, Super Admin.
