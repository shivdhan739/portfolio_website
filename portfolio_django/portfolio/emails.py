"""Sends the two contact-form emails: one to the admin, one confirmation to the visitor."""
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _send(subject, text, html, to, reply_to):
    mail = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to],
        reply_to=[reply_to],
    )
    mail.attach_alternative(html, "text/html")
    mail.send(fail_silently=False)


def send_contact_emails(msg):
    """Send both emails. Each one is tried separately so one failure never blocks the other."""
    errors = []
    phone_link = "".join(ch for ch in settings.PUBLIC_PHONE if ch.isdigit() or ch == "+")
    ctx = {
        "msg": msg,
        "admin_email": settings.ADMIN_EMAIL,
        "phone": settings.PUBLIC_PHONE,
        "phone_link": phone_link,
    }

    # 1) Notification to the admin (reply goes straight to the visitor)
    try:
        text = (
            "New message from your portfolio\n\n"
            f"Name: {msg.name}\nEmail: {msg.email}\nSubject: {msg.subject}\n\n{msg.message}\n"
        )
        _send(
            f"\U0001F514 New portfolio message from {msg.name} - {msg.subject}",
            text,
            render_to_string("emails/admin_notification.html", ctx),
            settings.ADMIN_EMAIL,
            msg.email,
        )
        msg.admin_mail_sent = True
    except Exception as exc:  # noqa: BLE001
        logger.exception("Admin notification email failed")
        errors.append(f"admin mail: {exc}")

    # 2) Confirmation to the visitor
    try:
        text = (
            f"Hi {msg.name},\n\nThank you for reaching out! I have received your message "
            "and will reply to you soon.\n\n"
            f"Your message:\nSubject: {msg.subject}\n{msg.message}\n\n"
            f"Regards,\nShivdhan Shirgole\nPython Full Stack Developer\n"
            f"{settings.ADMIN_EMAIL} | {settings.PUBLIC_PHONE}\n"
        )
        _send(
            "Thank you for contacting me, " + msg.name.split(" ")[0] + "! \U0001F64C",
            text,
            render_to_string("emails/user_confirmation.html", ctx),
            msg.email,
            settings.ADMIN_EMAIL,
        )
        msg.user_mail_sent = True
    except Exception as exc:  # noqa: BLE001
        logger.exception("Visitor confirmation email failed")
        errors.append(f"user mail: {exc}")

    msg.email_error = "\n".join(errors)
    msg.save(update_fields=["admin_mail_sent", "user_mail_sent", "email_error"])
    return msg.admin_mail_sent, msg.user_mail_sent
