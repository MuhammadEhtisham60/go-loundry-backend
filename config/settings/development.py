from .base import *

DEBUG = True

# Database
# Use DATABASE_URL if configured, otherwise fallback to local sqlite3 for easier development
DATABASES = {
    "default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR}/db.sqlite3")
}

# CORS Settings
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "http://localhost:3000",
        "http://localhost:3008",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3008",
        "http://localhost:8000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://go-loundry-frontend.netlify.app",
    ],
)

# Email Backend for development: SMTP if credentials provided, console fallback otherwise
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend" if env("SMTP_USER", default="") else "django.core.mail.backends.console.EmailBackend")

