import logging
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .emails import send_contact_emails
from .forms import ContactForm
from .models import ContactMessage, Project

logger = logging.getLogger(__name__)
LIMIT_HOURS = 24  # one message per email address every 24 hours


def home(request):
    return render(request, "portfolio/home.html")


def about(request):
    return render(request, "portfolio/about.html")


def skills(request):
    return render(request, "portfolio/skills.html")


def projects(request):
    all_projects = Project.objects.filter(is_active=True)
    return render(request, "portfolio/projects.html", {"projects": all_projects})


def education(request):
    return render(request, "portfolio/education.html")


def contact(request):
    return render(request, "portfolio/contact.html")


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


@require_POST
def send_contact_message(request):
    """Contact form: saves the message, mails the admin and sends a thank-you mail to the visitor."""
    # Honeypot: bots fill this hidden field. Pretend success so they learn nothing.
    if request.POST.get("website"):
        messages.success(request, "Thank you! Your message was sent.")
        return redirect("contact")

    form = ContactForm(request.POST)
    if not form.is_valid():
        if "email" in form.errors:
            messages.error(request, "Please enter a valid email address.")
        elif "message" in form.errors and "max_length" in [e.code for e in form.errors["message"].as_data()]:
            messages.error(request, "Your message is too long (maximum 2000 characters).")
        else:
            messages.error(request, "Please fill in your name, email, subject and message.")
        return redirect("contact")

    data = form.cleaned_data
    since = timezone.now() - timedelta(hours=LIMIT_HOURS)
    if ContactMessage.objects.filter(email__iexact=data["email"], created_at__gte=since).exists():
        messages.error(
            request,
            "A message from this email was already sent in the last 24 hours. "
            f"Please try again later, or email me directly at {settings.PUBLIC_EMAIL}.",
        )
        return redirect("contact")

    msg = ContactMessage.objects.create(
        name=data["name"],
        email=data["email"],
        subject=data["subject"],
        message=data["message"],
        ip_address=_client_ip(request),
    )
    admin_ok, user_ok = send_contact_emails(msg)

    first_name = data["name"].split(" ")[0]
    text = f"Thank you, {first_name}! Your message was sent successfully."
    if user_ok:
        text += " A confirmation was sent to your email."
    # The message is saved in the admin panel even if an email failed, so it is never lost.
    messages.success(request, text)
    return redirect("contact")
