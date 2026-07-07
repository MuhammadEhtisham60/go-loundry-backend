# GoLaundry Backend Documentation

Welcome to the official technical documentation for the GoLaundry enterprise backend application. This system is designed as a production-ready, highly modular REST API built with Django and Django REST Framework.

## Project Structure & Documentation Indexes

Below is an index of all detailed module specifications, API references, and manuals:

1. **[Developer Guide](DEVELOPER_GUIDE.md)**: Details the design system, service layer abstractions, testing strategy, coding conventions, and setup guides.
2. **[API Reference Index](API_REFERENCE.md)**: A complete tabular index of all public, customer, and administrative endpoints.
3. **Module Guides**:
   - **[Authentication Module](authentication.md)**: Handles user registrations, phone/email logins, OTP verification codes, and OAuth mock logins.
   - **[Customers Module](customers.md)**: Admin-facing customer listing, blocking, and unblocking controls.
   - **[Addresses Module](addresses.md)**: Multi-address customer profile, automatic default flag rotating, and coordinates snapshots.
   - **[Locations & Warehouse Module](locations.md)**: Operational coverage radius checks and dynamic delivery charge bands.
   - **[Services Catalog Module](services_catalog.md)**: Laundry services list, soft deletions, and custom display sequence.
   - **[Orders Module](orders.md)**: Orders processing, item catalog tracking, distance calculations, cancellations, and reordering.
   - **[Reviews Module](reviews.md)**: Post-laundry rating reviews and order completeness bounds.
   - **[Support Chats Module](chats.md)**: Multi-user support rooms, text messaging, image file attachments, and agent assignment.
   - **[Notifications Module](notifications.md)**: SMS and FCM Push notification receipt log lookups.
   - **[Dashboard Stats Module](dashboard.md)**: Operational counts, revenue charts aggregates, and active chat volumes.
   - **[Analytical Reports Module](reports.md)**: Order summaries, completed revenues, customer statuses, and popularity lists.
   - **[Administration Module](administration.md)**: Back-office controls and user roles security configuration matrix.

---

## Technology Stack

- **Framework**: Django 5.0 + Django REST Framework (DRF) 3.15
- **Language**: Python 3.12+
- **Database**: PostgreSQL (Production) / SQLite (Fallback Developer Setup)
- **Security**: JWT Authentication (`djangorestframework-simplejwt`)
- **OpenAPI / Swagger Specs**: `drf-spectacular`
- **Environment Management**: `django-environ`
