"""Optional email backend that sends through Brevo's HTTPS API (port 443).

Render's FREE web services block SMTP ports (25/465/587), so Gmail SMTP only works on a
paid plan. With a free Brevo account you can set BREVO_API_KEY and emails go over HTTPS.
The sender (ADMIN_EMAIL) must be verified as a sender inside Brevo.
"""
import json
import logging
import urllib.error
import urllib.request
from email.utils import parseaddr

from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

logger = logging.getLogger(__name__)
API_URL = "https://api.brevo.com/v3/smtp/email"


class BrevoAPIBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        sent = 0
        for message in email_messages:
            try:
                self._send(message)
                sent += 1
            except Exception:
                logger.exception("Brevo API send failed")
                if not self.fail_silently:
                    raise
        return sent

    def _send(self, message):
        from_name, from_email = parseaddr(message.from_email)
        payload = {
            "sender": {"name": from_name or "Shivdhan Shirgole", "email": from_email},
            "to": [{"email": addr} for addr in message.to],
            "subject": message.subject,
            "textContent": message.body,
        }
        for content, mimetype in getattr(message, "alternatives", []):
            if mimetype == "text/html":
                payload["htmlContent"] = content
        if message.reply_to:
            payload["replyTo"] = {"email": parseaddr(message.reply_to[0])[1]}

        request = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "api-key": settings.BREVO_API_KEY,
                "accept": "application/json",
                "content-type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "ignore")[:300]
            raise RuntimeError(f"Brevo API error {exc.code}: {detail}") from exc
