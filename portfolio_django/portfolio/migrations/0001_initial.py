from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80)),
                ("email", models.EmailField(max_length=120)),
                ("subject", models.CharField(default="Portfolio contact", max_length=120)),
                ("message", models.TextField(max_length=2000)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_read", models.BooleanField(default=False)),
                ("admin_mail_sent", models.BooleanField(default=False, verbose_name="Mail to admin sent")),
                ("user_mail_sent", models.BooleanField(default=False, verbose_name="Confirmation to visitor sent")),
                ("email_error", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Contact message",
                "verbose_name_plural": "Contact messages",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("emoji", models.CharField(default="🚀", max_length=4)),
                ("tag", models.CharField(default="New", help_text="Small badge, e.g. Live / Django", max_length=20)),
                ("title", models.CharField(max_length=80)),
                ("description", models.CharField(max_length=400)),
                ("points", models.TextField(blank=True, help_text="Bullet points - one per line")),
                ("tech", models.CharField(blank=True, help_text="Comma separated, e.g. Python, Django, MySQL", max_length=200)),
                ("link", models.URLField(blank=True, help_text="Live demo link (optional)")),
                ("order", models.PositiveIntegerField(default=0, help_text="Lower number shows first")),
                ("is_active", models.BooleanField(default=True, help_text="Untick to hide from the website")),
            ],
            options={
                "ordering": ["order", "id"],
            },
        ),
    ]
