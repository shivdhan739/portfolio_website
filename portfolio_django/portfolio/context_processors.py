from django.conf import settings


def site(request):
    """Values every template needs (footer, contact page, hero links)."""
    phone = settings.PUBLIC_PHONE
    return {
        "public_email": settings.PUBLIC_EMAIL,
        "public_phone": phone,
        "phone_link": "".join(ch for ch in phone if ch.isdigit() or ch == "+"),
        "github_url": settings.GITHUB_URL,
    }
