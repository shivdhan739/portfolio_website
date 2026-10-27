from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=120)
    subject = models.CharField(max_length=120, default="Portfolio contact")
    message = models.TextField(max_length=2000)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    admin_mail_sent = models.BooleanField(default=False, verbose_name="Mail to admin sent")
    user_mail_sent = models.BooleanField(default=False, verbose_name="Confirmation to visitor sent")
    email_error = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact message"
        verbose_name_plural = "Contact messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Project(models.Model):
    emoji = models.CharField(max_length=4, default="🚀")
    tag = models.CharField(max_length=20, default="New", help_text="Small badge, e.g. Live / Django")
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=400)
    points = models.TextField(blank=True, help_text="Bullet points - one per line")
    tech = models.CharField(max_length=200, blank=True, help_text="Comma separated, e.g. Python, Django, MySQL")
    link = models.URLField(blank=True, help_text="Live demo link (optional)")
    order = models.PositiveIntegerField(default=0, help_text="Lower number shows first")
    is_active = models.BooleanField(default=True, help_text="Untick to hide from the website")

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def points_list(self):
        return [p.strip() for p in self.points.splitlines() if p.strip()]

    @property
    def tech_list(self):
        return [t.strip() for t in self.tech.split(",") if t.strip()]
