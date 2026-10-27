from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Send a test email to check the email settings: python manage.py test_email you@example.com"

    def add_arguments(self, parser):
        parser.add_argument("to", nargs="?", default=settings.ADMIN_EMAIL)

    def handle(self, *args, **options):
        self.stdout.write(f"Backend: {settings.EMAIL_BACKEND}")
        sent = send_mail(
            "Portfolio test email",
            "If you can read this, your email settings work.",
            settings.DEFAULT_FROM_EMAIL,
            [options["to"]],
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS(f"Sent {sent} email to {options['to']}"))
