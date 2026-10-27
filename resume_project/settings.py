"""Django settings for Shivdhan's portfolio (project package: resume_project)."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def _load_env_file(path):
    """Tiny .env reader (no package needed). Survives Notepad/PowerShell encodings (UTF-8 BOM, UTF-16)
    and never crashes the site: a bad line is simply skipped. Real environment variables win."""
    try:
        raw = path.read_bytes()
    except OSError:
        return
    text = None
    for encoding in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeError:
            continue
    if text is None:
        return
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if key.startswith("export "):
            key = key[7:].strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        elif " #" in value:
            value = value.split(" #")[0].strip()
        if key:
            os.environ.setdefault(key, value)


_load_env_file(BASE_DIR / ".env")

# These two helpers are optional locally: if one is not installed the site still starts
# (so a half-finished "pip install" can never break `runserver`). On Render they are installed.
try:
    import dj_database_url
except ImportError:
    dj_database_url = None

try:
    import whitenoise  # noqa: F401
    HAS_WHITENOISE = True
except ImportError:
    HAS_WHITENOISE = False


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


def env_list(name):
    return [x.strip() for x in os.environ.get(name, "").split(",") if x.strip()]


# Render sets RENDER=true automatically, so production is safe by default.
ON_RENDER = "RENDER" in os.environ
DEBUG = env_bool("DEBUG", default=not ON_RENDER)
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-insecure-key-change-me")

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"] + env_list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")
RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_HOST:
    ALLOWED_HOSTS.append(RENDER_HOST)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_HOST}")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "portfolio",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    *(["whitenoise.middleware.WhiteNoiseMiddleware"] if HAS_WHITENOISE else []),
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "resume_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "portfolio.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "resume_project.wsgi.application"

# ---------- Database: SQLite locally, PostgreSQL on Render (DATABASE_URL) ----------
if dj_database_url:
    DATABASES = {
        "default": dj_database_url.config(
            default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ---------- Static files (WhiteNoise serves them on Render) ----------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG or not HAS_WHITENOISE
            else "whitenoise.storage.CompressedStaticFilesStorage"
        )
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------- Email ----------
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "shivdhanshirgole2808@gmail.com")
PUBLIC_EMAIL = os.environ.get("PUBLIC_EMAIL", "shivdhanshirgole085@gmail.com")  # shown on the page
PUBLIC_PHONE = os.environ.get("PUBLIC_PHONE", "+91-9049418836")
GITHUB_URL = os.environ.get("GITHUB_URL", "https://github.com/shivdhan739")

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", ADMIN_EMAIL)
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "").replace(" ", "")
EMAIL_TIMEOUT = 15
BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")
DEFAULT_FROM_EMAIL = f"Shivdhan Shirgole <{EMAIL_HOST_USER}>"
SERVER_EMAIL = EMAIL_HOST_USER
CONTACT_EMAIL = ADMIN_EMAIL  # contact form messages are delivered here

if BREVO_API_KEY:
    # HTTPS API (port 443) - portfolio ऍपच्या आत email_backends फाईल आहे
    EMAIL_BACKEND = "portfolio.email_backends.BrevoAPIBackend"
elif EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    # No credentials yet: emails are printed in the terminal (handy for local testing)
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ---------- Security in production ----------
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"portfolio": {"handlers": ["console"], "level": "INFO"}},
}
