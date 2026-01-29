import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

EMAIL = os.getenv("LOGAN_EMAIL")
PASSWORD = os.getenv("LOGAN_EMAIL_PASSWORD")

def handle_email_command(command=None, *, to=None, subject=None, message=None):
    if not EMAIL or not PASSWORD:
        return "Email credentials are not configured."
    """
    Robust email sender.
    Accepts either:
    - to="email"
    OR
    - to={ "to": "...", "subject": "...", "body": "..." }
    """

    try:
        # 🛡️ DEFENSIVE FIX: unpack dict if passed wrongly
        if isinstance(to, dict):
            subject = to.get("subject")
            message = to.get("body")
            to = to.get("to")

        if not isinstance(to, str):
            return "Invalid email address."

        msg = EmailMessage()
        msg["From"] = EMAIL
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL.strip(), PASSWORD.strip())
            server.send_message(msg)

        # Episodic logging (non-blocking)
        try:
            from core.episodic_memory import log_event
            log_event(
                "email_sent",
                f"Email sent to {to} with subject '{subject}'"
            )
        except Exception as e:
            print("Episodic log failed:", e)

        return f"Email sent successfully to {to}."

    except Exception as e:
        print("SMTP ERROR:", e)
        return "Failed to send email."
