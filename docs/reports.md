# Reports & Analytics Module

## Purpose
Generates compiled data tables and analytical breakdowns for business planning, billing audits, and geographical analysis.

---

## Business Rules

- Access restricted exclusively to `ADMIN` and `SUPER_ADMIN` roles.
- `SUPPORT_AGENT` and `CUSTOMER` roles receive a `403 Forbidden` response.
- Generates reports on:
  - Orders: volume status breakdowns over time.
  - Revenue: sum of completed cash collections and shipping fee captures.
  - Customer: total client registration counts.
  - Service: popularity rankings based on order frequency and sales volumes.
  - Zones: operational distance band reviews to evaluate logistics efficiency.

---

## Endpoints

### Get Orders Report
`GET /api/admin/reports/orders/?date_from=2026-06-01&date_to=2026-06-30`

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Orders report compiled successfully.",
  "data": {
    "date_range": { "from": "2026-06-01", "to": "2026-06-30" },
    "total_orders": 25,
    "status_breakdown": {
      "DELIVERED": 20,
      "CANCELLED": 5
    }
  }
}
```

---

### Get Geographical Zone Report
`GET /api/admin/reports/zones/`

#### Success Response (200 OK)
```json
{
  "success": true,
  "message": "Geographical zone report compiled.",
  "data": [
    {
      "zone_band": "0 - 5 KM",
      "total_orders": 15,
      "estimated_revenue": 3400.00
    },
    {
      "zone_band": "5 - 10 KM",
      "total_orders": 10,
      "estimated_revenue": 2100.00
    }
  ]
}
```
