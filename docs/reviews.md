# Reviews Module

## Purpose
Collects and displays customer satisfaction scores and feedback remarks for completed orders.

---

## Models

### Review

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| user | FK(User) | Customer reviewer |
| order | OneToOne(Order) | Target order rated |
| rating | Integer | Score from 1 to 5 |
| remarks | Text | Feedback message |
| created_at | DateTime | Timestamp |

---

## Business Rules

- Customers can submit a review only if the order status is `DELIVERED`.
- Customers can only review orders that they placed (ownership check).
- A maximum of **one** review can be created per order (1-to-1 database constraint).
- Scores must fall within the range `1` to `5` inclusive.

---

## Endpoints

### Submit Review
`POST /api/reviews/`

#### Request Payload
```json
{
  "order_id": "c018a1be-7443-41bb-b054-d83bebf0f9d9",
  "rating": 5,
  "remarks": "Clean and fresh clothes! Thanks!"
}
```

#### Success Response (201 Created)
```json
{
  "success": true,
  "message": "Review submitted successfully.",
  "data": {
    "id": "e9e4f5a3-7e4f-4d3a-b8fb-47dbfa8f01b1",
    "order": "c018a1be-7443-41bb-b054-d83bebf0f9d9",
    "rating": 5,
    "remarks": "Clean and fresh clothes! Thanks!"
  }
}
```

#### Error Response (400 Validation Error - Already reviewed)
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": [
    "You have already reviewed this order."
  ]
}
```
