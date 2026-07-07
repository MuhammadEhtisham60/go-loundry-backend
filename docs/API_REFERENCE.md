# API Reference Index

This document maps all backend REST API routes, HTTP methods, and required security roles.

| Module | Endpoint | Method | Role Allowed | Description |
|---|---|---|---|---|
| **Auth** | `/api/auth/register/` | POST | Public | Registers a new Customer account |
| **Auth** | `/api/auth/login/` | POST | Public | Authenticates via email/phone + password |
| **Auth** | `/api/auth/login/otp/` | POST | Public | Requests an OTP code to be sent |
| **Auth** | `/api/auth/login/otp/verify/` | POST | Public | Validates OTP and returns JWT tokens |
| **Auth** | `/api/auth/profile/` | GET | Authenticated | Retrieves profile information |
| **Auth** | `/api/auth/profile/` | PUT | Authenticated | Updates full name or avatar |
| **Addresses** | `/api/addresses/` | GET | Customer | Lists customer addresses |
| **Addresses** | `/api/addresses/` | POST | Customer | Adds an address to customer profile |
| **Addresses** | `/api/addresses/<uuid:pk>/` | DELETE | Customer | Deletes an address |
| **Locations** | `/api/locations/warehouse/` | GET | Public | Gets warehouse location details |
| **Locations** | `/api/locations/warehouse/` | PUT | Super Admin | Updates warehouse location/radius |
| **Locations** | `/api/locations/validate-area/` | POST | Public | Checks if coords are in serviced area |
| **Catalog** | `/api/services/` | GET | Public | Lists all active laundry services |
| **Catalog** | `/api/services/` | POST | Admin / Super Admin | Creates a laundry service |
| **Catalog** | `/api/services/reorder/` | POST | Admin / Super Admin | Reorders sequence presentation |
| **Orders** | `/api/orders/` | GET | Authenticated | Lists orders (Customers own, Admins all) |
| **Orders** | `/api/orders/` | POST | Customer | Places a new laundry order |
| **Orders** | `/api/orders/<uuid:pk>/` | GET | Authenticated | Retrieves order details |
| **Orders** | `/api/orders/<uuid:pk>/cancel/` | POST | Authenticated | Cancels an order |
| **Orders** | `/api/orders/<uuid:pk>/status/` | PUT | Support / Admin | Updates status and maps rider |
| **Orders** | `/api/orders/<uuid:pk>/reorder/` | POST | Customer | Pre-fills a new order from previous |
| **Reviews** | `/api/reviews/` | GET | Authenticated | Lists reviews (Customers own, Admins all) |
| **Reviews** | `/api/reviews/` | POST | Customer | Rates a completed order |
| **Chats** | `/api/chats/conversations/` | GET | Authenticated | Lists support conversations |
| **Chats** | `/api/chats/conversations/` | POST | Customer | Starts/Retrieves support session |
| **Chats** | `/api/chats/conversations/<id>/messages/` | GET | Authenticated | Gets chat thread message logs |
| **Chats** | `/api/chats/conversations/<id>/messages/` | POST | Authenticated | Sends a chat message/image |
| **Chats** | `/api/chats/conversations/<id>/assign/` | POST | Support / Admin | Assigns support agent |
| **Chats** | `/api/chats/conversations/<id>/resolve/` | POST | Support / Admin | Marks conversation resolved |
| **Notifications**| `/api/notifications/` | GET | Customer | Lists notification SMS/FCM logs |
| **Dashboard** | `/api/admin/dashboard/stats/` | GET | Support / Admin | Compiles operational statistics |
| **Reports** | `/api/admin/reports/orders/` | GET | Admin / Super Admin | Compiles orders volume reports |
| **Reports** | `/api/admin/reports/revenue/` | GET | Admin / Super Admin | Compiles financial revenue reports |
| **Reports** | `/api/admin/reports/customers/` | GET | Admin / Super Admin | Compiles customer signups reports |
| **Reports** | `/api/admin/reports/services/` | GET | Admin / Super Admin | Compiles service popularity reports |
| **Reports** | `/api/admin/reports/zones/` | GET | Admin / Super Admin | Compiles logistics zone reports |
