# Go Laundry Backend

A production-ready Django REST Framework backend project with a clean, scalable, and enterprise-grade modular architecture.

## Architecture

This project is built around clean architecture principles and a decoupled modular structure:

- **Modular Components**: Custom apps are isolated inside the `apps/` directory (e.g., `apps/authentication/`).
- **Services Pattern**: Business logic is decoupled from both views and serializers, residing inside service classes (`services/auth_service.py`).
- **Standardized Response Envelope**: All API endpoints return a unified payload structure via custom responses and custom exception handling:
  - **Success Response**:
    ```json
    {
      "success": true,
      "data": { ... },
      "message": "Operation completed successfully.",
      "errors": null
    }
    ```
  - **Error Response**:
    ```json
    {
      "success": false,
      "data": null,
      "message": "Validation failed",
      "errors": {
        "email": ["A user with this email address already exists."]
      }
    }
    ```

---

## Tech Stack

- **Core**: Python 3.12+, Django 5.0, Django REST Framework 3.15
- **Authentication**: JWT using SimpleJWT
- **Database**: PostgreSQL (with SQLite fallback in local development)
- **Configuration**: Environment variables using django-environ
- **CORS**: django-cors-headers

---

## Getting Started

### Prerequisites

- Python 3.12 or higher installed.
- PostgreSQL database (optional for development, SQLite is used by default if no connection string is provided).

### Local Setup

1. **Clone the Repository & Navigate to Project Root**:
   ```bash
   cd go-laundry-backend
   ```

2. **Create and Activate a Virtual Environment**:
   * Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Copy `.env.example` to `.env` and update the database credentials and secret keys:
   ```bash
   cp .env.example .env
   ```

5. **Apply Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser (Optional - for Admin Access)**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   The backend will be available at `http://127.0.0.1:8000/`.

---

## Running Tests

To run the full test suite with coverage:
```bash
python manage.py test
```

---

## API Endpoints

### 1. User Registration
* **Endpoint**: `POST /api/auth/register/`
* **Authentication**: None
* **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "password_confirm": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```
* **Success Response (201 Created)**:
  ```json
  {
    "success": true,
    "data": {
      "id": "e4b2d56a-1234-5678-abcd-ef0123456789",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "created_at": "2026-06-27T09:24:40.000Z",
      "updated_at": "2026-06-27T09:24:40.000Z"
    },
    "message": "User registered successfully.",
    "errors": null
  }
  ```

### 2. User Login
* **Endpoint**: `POST /api/auth/login/`
* **Authentication**: None
* **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }
  ```
* **Success Response (200 OK)**:
  ```json
  {
    "success": true,
    "data": {
      "tokens": {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
      },
      "user": {
        "id": "e4b2d56a-1234-5678-abcd-ef0123456789",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "created_at": "2026-06-27T09:24:40.000Z",
        "updated_at": "2026-06-27T09:24:40.000Z"
      }
    },
    "message": "Login successful.",
    "errors": null
  }
  ```

### 3. Refresh Access Token
* **Endpoint**: `POST /api/auth/token/refresh/`
* **Authentication**: None
* **Request Body**:
  ```json
  {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
* **Success Response (200 OK)**:
  ```json
  {
    "success": true,
    "data": {
      "access": "new_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    },
    "message": "Token refreshed successfully.",
    "errors": null
  }
  ```

### 4. Get User Profile
* **Endpoint**: `GET /api/auth/profile/`
* **Authentication**: Bearer Token (`Authorization: Bearer <access_token>`)
* **Success Response (200 OK)**:
  ```json
  {
    "success": true,
    "data": {
      "id": "e4b2d56a-1234-5678-abcd-ef0123456789",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "created_at": "2026-06-27T09:24:40.000Z",
      "updated_at": "2026-06-27T09:24:40.000Z"
    },
    "message": "Profile retrieved successfully.",
    "errors": null
  }
  ```
