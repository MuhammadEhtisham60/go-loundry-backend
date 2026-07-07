# Developer Guide

Welcome to the GoLaundry backend developer guide! This document explains our backend architecture patterns, layers separation, testing standards, and extension paths.

---

## 1. Project Architecture

The codebase separates queries and mutations cleanly using the **Selector-Service Pattern** (similar to CQRS):
- **Models**: Standard Django database definitions without heavy business logic.
- **Services (`services/`)**: Implement mutation operations (writes, creations, updates, external API calls, transactional integrity).
- **Selectors (`selectors/`)**: Handle query and read operations (filtering, complex aggregations, database joins, prefetch optimizations).
- **Views**: Handle HTTP routing, parsing parameters, call Services/Selectors, and return standard JSON formats.

```mermaid
graph TD
    Client[REST Client / Frontend] --> Views[Views & Serializers]
    Views --> Selectors[Selectors (Reads)]
    Views --> Services[Services (Writes)]
    Selectors --> Database[(PostgreSQL)]
    Services --> Database
```

---

## 2. Layer Conventions

### Services
- Must be annotated with `@staticmethod`.
- Utilize `transaction.atomic` blocks for any operations writing to multiple tables.
- Raise `serializers.ValidationError` for business rule violations (e.g. out of service area).

### Selectors
- Must return Django `QuerySet` or structured dictionaries.
- Utilize `.select_related()` and `.prefetch_related()` to prevent `N+1` query leaks.

### Response Wrappers
All outputs are intercepted and returned in a unified envelope:
```json
{
  "success": true,
  "message": "Descriptive text",
  "data": { ... },
  "errors": null
}
```

---

## 3. Testing Strategy

- **Test Suite**: Every application contains a `tests/` folder with `test_*.py` test suites.
- **Run Command**:
  ```bash
  python manage.py test
  ```
- All test suites inherit from `rest_framework.test.APITestCase` and authenticate endpoints using `self.client.force_authenticate`.

---

## 4. Coding Conventions

- **Variable Names**: snake_case for Python parameters, camelCase for API JSON parameters (automatic mapping).
- **Class Names**: PascalCase (e.g. `OrderService`).
- **Database Tables**: Pluralized snake_case (e.g. `order_items`).
