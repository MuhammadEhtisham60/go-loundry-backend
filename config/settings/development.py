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
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ],
)

# Email Backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
