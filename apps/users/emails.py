import string
import secrets
import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = logging.getLogger(__name__)


def generate_password(length: int = 12) -> str:
    """
    Generate a cryptographically secure random password containing
    uppercase, lowercase, digits, and symbols.
    """
    alphabet = string.ascii_letters + string.digits + "!@#$%&*"
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        # Ensure at least one of each required character type
        if (
            any(c.isupper() for c in password)
            and any(c.islower() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in "!@#$%&*" for c in password)
        ):
            return password


def send_team_member_credentials(full_name: str, email: str, password: str, role_name: str) -> bool:
    """
    Send a welcome email containing login credentials to a newly created team member.
    Returns True on success, False on failure.
    """
    subject = "Welcome to GoLaundry — Your Account Credentials"
    from_email = settings.DEFAULT_FROM_EMAIL

    # ── Plain-text fallback ──────────────────────────────────────────────────
    text_body = f"""
Hello {full_name},

Your GoLaundry back-office account has been created.

Login URL : http://localhost:5173/login
Email     : {email}
Password  : {password}
Role      : {role_name}

Please change your password after your first login.

— GoLaundry Team
""".strip()

    # ── HTML version ─────────────────────────────────────────────────────────
    html_body = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Your GoLaundry Account</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f0f4f8; color: #1a1a1a; margin: 0; padding: 0; }}
    .wrapper {{ max-width: 560px; margin: 40px auto; background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 24px rgba(53,179,220,0.12); border: 1px solid #e2f4fb; }}
    .header {{ background: linear-gradient(135deg, #35b3dc, #27c6e8); padding: 36px 32px; text-align: center; }}
    .header h1 {{ margin: 0; font-size: 26px; color: #ffffff; font-weight: 800; letter-spacing: -0.5px; }}
    .header p {{ margin: 6px 0 0; font-size: 13px; color: rgba(255,255,255,0.80); letter-spacing: 0.5px; text-transform: uppercase; }}
    .body {{ padding: 32px; background: #ffffff; }}
    .greeting {{ font-size: 15px; margin-bottom: 20px; color: #374151; line-height: 1.6; }}
    .creds {{ background: #f7fbfe; border: 1px solid #d0edf8; border-radius: 12px; padding: 4px 20px; margin: 20px 0; }}
    .cred-row {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #e8f4fb; }}
    .cred-row:last-child {{ border-bottom: none; }}
    .cred-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1.2px; color: #9ca3af; font-weight: 600; }}
    .cred-value {{ font-size: 14px; font-weight: 700; color: #35b3dc; font-family: 'Courier New', Courier, monospace; word-break: break-all; text-align: right; max-width: 60%; }}
    .btn {{ display: inline-block; margin-top: 24px; padding: 14px 32px; background: #35b3dc; color: #ffffff; text-decoration: none; border-radius: 10px; font-weight: 700; font-size: 14px; letter-spacing: 0.3px; }}
    .btn:hover {{ background: #27a0c8; }}
    .notice {{ margin-top: 24px; font-size: 12px; color: #6b7280; line-height: 1.7; padding: 12px 16px; background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; }}
    .footer {{ padding: 20px 32px; background: #f9fafb; border-top: 1px solid #e5e7eb; text-align: center; font-size: 11px; color: #9ca3af; }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <h1>GoLaundry</h1>
      <p>Back-Office Portal</p>
    </div>
    <div class="body">
      <p class="greeting">Hello <strong>{full_name}</strong>,<br/>Your account has been created on the GoLaundry admin portal. Use the credentials below to log in.</p>
      <div class="creds">
        <div class="cred-row">
          <span class="cred-label">Email</span>
          <span class="cred-value">{email}</span>
        </div>
        <div class="cred-row">
          <span class="cred-label">Password</span>
          <span class="cred-value">{password}</span>
        </div>
        <div class="cred-row">
          <span class="cred-label">Role</span>
          <span class="cred-value">{role_name}</span>
        </div>
      </div>
      <a href="http://localhost:5173/login" class="btn">Login to Portal →</a>
      <p class="notice">⚠️ Please change your password immediately after your first login. Do not share these credentials with anyone.</p>
    </div>
    <div class="footer">© GoLaundry. This email was sent automatically — please do not reply.</div>
  </div>
</body>
</html>
""".strip()

    try:
        msg = EmailMultiAlternatives(subject, text_body, from_email, [email])
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
        logger.info("Credentials email sent to %s", email)
        return True
    except Exception as exc:
        logger.error("Failed to send credentials email to %s: %s", email, exc)
        return False
