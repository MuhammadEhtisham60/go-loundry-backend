# 🔐 GoLaundry Authentication API Flow & Postman Testing Guide

This guide describes how to configure, run, and test authentication flows using the GoLaundry Postman collection. It maps the variables, endpoints, request payloads, and response structures for all security-related workflows.

---

## 🛠️ Postman Collection Setup

The GoLaundry collection is configured to handle JWT token lifecycles automatically. The collection defines three primary variables that manage client environments:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `base_url` | `http://127.0.0.1:8000` | The address of the running backend server. |
| `access_token` | `paste_access_token_here` | The temporary JWT token used to authenticate protected endpoints. |
| `refresh_token` | `paste_refresh_token_here` | The long-lived JWT token used to request a new access token. |

> [!TIP]
> **Zero Manual Copy-Paste**: We have pre-configured Postman **Tests Scripts** (post-request hooks) directly inside [GoLaundry.postman_collection.json](./GoLaundry.postman_collection.json) and [golaundry_api_collection.json](../golaundry_api_collection.json). Whenever you execute any login, OTP verification, or social authentication requests, Postman will dynamically update `access_token` and `refresh_token` in your collection variables.

---

## 🔄 Authentication Flows

### Flow A: Email & Password Authentication (Standard Customer Sign-up/Sign-in)
This is the standard authentication workflow for customers using conventional email and password credentials.

1. **Register**: Send a `POST` request to `{{base_url}}/api/auth/register/` to create a new user profile.
2. **Login**: Send a `POST` request to `{{base_url}}/api/auth/login/` containing the credentials.
   - *Postman Automation*: If the login is successful, Postman automatically extracts the `access` and `refresh` tokens from the response and saves them to `access_token` and `refresh_token` collection variables.
3. **Authorized Request**: Access any protected endpoint (like `/api/auth/profile/` or `/api/addresses/`). The request will automatically utilize `Bearer {{access_token}}` from the collection variables.

### Flow B: OTP (Mobile) Authentication (Passwordless Login)
This flow allows logging in using a dynamic one-time password (OTP) sent to the user's phone.

1. **Trigger OTP**: Send a `POST` request to `{{base_url}}/api/auth/login/otp/` with the user's mobile number.
2. **Verify OTP**: Send a `POST` request to `{{base_url}}/api/auth/login/otp/verify/` with the mobile number and the OTP code.
   - *Postman Automation*: Upon successful verification, Postman extracts and updates the collection's `access_token` and `refresh_token`.

### Flow C: Social Login (Google & Facebook Mock)
Simulates Google or Facebook Single Sign-On (SSO) by sending an OAuth provider token.

1. **Social Login**: Send a `POST` request to `{{base_url}}/api/auth/social-login/` with the platform (`GOOGLE` or `FACEBOOK`) and OAuth token details.
   - *Postman Automation*: Extracts and updates the `access_token` and `refresh_token` collection variables.

### Flow D: Token Expiration & Refreshing
Access tokens are short-lived. Once a request returns a `401 Unauthorized` token expiry response:

1. **Refresh Token**: Send a `POST` request to `{{base_url}}/api/auth/token/refresh/` passing the current `refresh_token`.
   - *Postman Automation*: Extracts the new `access` token from the response data and automatically sets the `access_token` variable.

### Flow E: Forgot & Reset Password
Use this flow if a user forgets their password and wants to define a new one.

1. **Forgot Password**: Send a `POST` request to `{{base_url}}/api/auth/forgot-password/` with the registered email. This sends a password reset OTP.
2. **Reset Password**: Send a `POST` request to `{{base_url}}/api/auth/reset-password/` containing the OTP code and new passwords.

---

## 📋 Endpoint Reference

This section details request and response examples for each endpoint defined in the authentication package.

### 1. Register User
Registers a new customer account.

- **HTTP Method**: `POST`
- **URL**: `{{base_url}}/api/auth/register/`
- **Access**: Public
- **Handler View**: [RegisterView](file:///c:/Users/l/Documents/MARN/products/live-version/go-loundry-backend/apps/authentication/views/register_view.py#L13)

**Request Body**:
```json
{
  "email": "customer@example.com",
  "phone": "03001234567",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Success Response (`201 Created`)**:
```json
{
  "success": true,
  "message": "User registered successfully.",
  "data": {
    "id": "e98e4e94-c782-4f3b-a5cc-efdc5456f91f",
    "email": "customer@example.com",
    "phone": "03001234567",
    "full_name": "John Doe",
    "role": "CUSTOMER"
  }
}
```

**Error Response (`400 Bad Request` - Validation Error)**:
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "phone": ["A user with this phone number already exists."]
  }
}
```

---

### 2. Login User (Password)
Logs in using email/phone and password.

- **HTTP Method**: `POST`
- **URL**: `{{base_url}}/api/auth/login/`
- **Access**: Public
- **Handler View**: [LoginView](file:///c:/Users/l/Documents/MARN/products/live-version/go-loundry-backend/apps/authentication/views/login_view.py#L13)

**Request Body**:
```json
{
  "email": "customer@example.com",
  "password": "SecurePassword123!"
}
```

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "tokens": {
      "access": "eyJhbGciOi...",
      "refresh": "eyJhbGciOi..."
    },
    "user": {
      "id": "e98e4e94-c782-4f3b-a5cc-efdc5456f91f",
      "email": "customer@example.com",
      "phone": "03001234567",
      "full_name": "John Doe"
    }
  }
}
```

---

### 3. Trigger OTP
Triggers the sending of an OTP verification code.

- **HTTP Method**: `POST`
- **URL**: `{{base_url}}/api/auth/login/otp/`
- **Access**: Public
- **Handler View**: [OtpTriggerView](file:///c:/Users/l/Documents/MARN/products/live-version/go-loundry-backend/apps/authentication/views/otp_view.py#L16)

**Request Body**:
```json
{
  "phone": "03001234567"
}
```

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "Verification OTP sent successfully.",
  "data": null
}
```

---

### 4. Verify OTP & Login
Validates the OTP code to log the user in.

- **HTTP Method**: `POST`
- **URL**: `{{base_url}}/api/auth/login/otp/verify/`
- **Access**: Public
- **Handler View**: [OtpVerifyView](file:///c:/Users/l/Documents/MARN/products/live-version/go-loundry-backend/apps/authentication/views/otp_view.py#L39)

**Request Body**:
```json
{
  "phone": "03001234567",
  "otp_code": "123456"
}
```

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "OTP verified and login successful.",
  "data": {
    "tokens": {
      "access": "eyJhbGciOi...",
      "refresh": "eyJhbGciOi..."
    },
    "user": {
      "id": "e98e4e94-c782-4f3b-a5cc-efdc5456f91f",
      "email": "customer@example.com",
      "phone": "03001234567",
      "full_name": "John Doe"
    }
  }
}
```

---

### 5. Social Login (Google/FB Mock)
Simulates standard social OAuth.

- **HTTP Method**: `POST`
- **URL**: `{{base_url}}/api/auth/social-login/`
- **Access**: Public
- **Handler View**: [SocialLoginView](file:///c:/Users/l/Documents/MARN/products/live-version/go-loundry-backend/apps/authentication/views/social_view.py#L13)

**Request Body**:
```json
{
  "platform": "GOOGLE",
  "token": "mock-oauth-token-string",
  "email": "oauthuser@example.com",
  "full_name": "Google User"
}
```

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "Social login successful.",
  "data": {
    "tokens": {
      "access": "eyJhbGciOi...",
      "refresh": "eyJhbGciOi..."
    },
    "user": {
      "id": "a98a4e94-c782-4f3b-a5cc-efdc5456f91f",
      "email": "oauthuser@example.com",
      "full_name": "Google User"
    }
  }
}
```

---

### 6. Get Profile
Retrieves detailed profile metadata for the authenticated user.

- **HTTP Method**: `GET`
- **URL**: `{{base_url}}/api/auth/profile/`
- **Access**: Authenticated (`Authorization: Bearer {{access_token}}`)
- **Handler View**: [ProfileView](file:///c:/Users/l/Documents/MARN/products/live-version/go-loundry-backend/apps/authentication/views/profile_view.py#L11)

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "Profile retrieved successfully.",
  "data": {
    "id": "e98e4e94-c782-4f3b-a5cc-efdc5456f91f",
    "email": "customer@example.com",
    "phone": "03001234567",
    "full_name": "John Doe",
    "role": "CUSTOMER"
  }
}
```

**Error Response (`401 Unauthorized` - Token Invalid or Expired)**:
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

---

### 7. Update Profile
Updates the profile information.

- **HTTP Method**: `PUT`
- **URL**: `{{base_url}}/api/auth/profile/`
- **Access**: Authenticated (`Authorization: Bearer {{access_token}}`)
- **Handler View**: [ProfileView](file:///c:/Users/l/Documents/MARN/products/live-version/go-loundry-backend/apps/authentication/views/profile_view.py#L11)

**Request Body**:
```json
{
  "full_name": "Johnathan Doe",
  "profile_photo": "https://images.example.com/avatar.jpg"
}
```

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "Profile updated successfully.",
  "data": {
    "id": "e98e4e94-c782-4f3b-a5cc-efdc5456f91f",
    "email": "customer@example.com",
    "phone": "03001234567",
    "full_name": "Johnathan Doe",
    "role": "CUSTOMER",
    "profile_photo": "https://images.example.com/avatar.jpg"
  }
}
```

---

### 8. Refresh Token
Exchanges a long-lived refresh token for a new short-lived access token.

- **HTTP Method**: `POST`
- **URL**: `{{base_url}}/api/auth/token/refresh/`
- **Access**: Public
- **Handler View**: [CustomTokenRefreshView](file:///c:/Users/l/Documents/MARN/products/live-version/go-loundry-backend/apps/authentication/views/token_refresh_view.py#L8)

**Request Body**:
```json
{
  "refresh": "{{refresh_token}}"
}
```

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "Token refreshed successfully.",
  "data": {
    "access": "eyJhbGciOi..."
  }
}
```

---

### 9. Forgot Password (Code Request)
Submits a password reset request code via email or phone.

- **HTTP Method**: `POST`
- **URL**: `{{base_url}}/api/auth/forgot-password/`
- **Access**: Public
- **Handler View**: [ForgotPasswordView](file:///c:/Users/l/Documents/MARN/products/live-version/go-loundry-backend/apps/authentication/views/password_reset_view.py#L15)

**Request Body**:
```json
{
  "email": "customer@example.com"
}
```

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "Password reset verification code sent.",
  "data": null
}
```

---

### 10. Reset Password
Resets password with the code sent using the Forgot Password endpoint.

- **HTTP Method**: `POST`
- **URL**: `{{base_url}}/api/auth/reset-password/`
- **Access**: Public
- **Handler View**: [ResetPasswordView](file:///c:/Users/l/Documents/MARN/products/live-version/go-loundry-backend/apps/authentication/views/password_reset_view.py#L38)

**Request Body**:
```json
{
  "email": "customer@example.com",
  "otp_code": "123456",
  "new_password": "NewSecurePassword123!",
  "password_confirm": "NewSecurePassword123!"
}
```

**Success Response (`200 OK`)**:
```json
{
  "success": true,
  "message": "Password has been reset successfully.",
  "data": null
}
```

---

## 🧪 Postman Scripts Reference (Under the Hood)

For reference, these are the scripts that have been dynamically injected into the JSON collection items. They handle saving/refreshing tokens on your active Postman workspace:

### On login-type requests (`Login User`, `Verify OTP`, and `Social Login`):
```javascript
if (pm.response.code === 200) {
    var response = pm.response.json();
    if (response.success && response.data && response.data.tokens) {
        pm.collectionVariables.set("access_token", response.data.tokens.access);
        pm.collectionVariables.set("refresh_token", response.data.tokens.refresh);
        console.log("Access and Refresh tokens updated successfully.");
    }
}
```

### On token refresh requests (`Refresh Token`):
```javascript
if (pm.response.code === 200) {
    var response = pm.response.json();
    if (response.success && response.data && response.data.access) {
        pm.collectionVariables.set("access_token", response.data.access);
        console.log("Access token refreshed and updated successfully.");
    }
}
```
