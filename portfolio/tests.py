from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactMessage, Project


class PageTests(TestCase):
    def test_all_pages_open(self):
        for name in ("home", "about", "skills", "projects", "education", "contact"):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)

    def test_projects_page_lists_seeded_projects(self):
        self.assertGreaterEqual(Project.objects.count(), 6)
        response = self.client.get(reverse("projects"))
        self.assertContains(response, "Online Job Portal")


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class ContactFormTests(TestCase):
    payload = {
        "name": "Test Visitor",
        "email": "visitor@example.com",
        "subject": "Python Developer opening",
        "message": "Hello Shivdhan, we would like to talk.",
    }

    def test_both_emails_are_sent(self):
        response = self.client.post(reverse("send_contact_message"), self.payload)
        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(len(mail.outbox), 2)
        admin_mail, visitor_mail = mail.outbox
        self.assertEqual(admin_mail.to, ["shivdhanshirgole2808@gmail.com"])
        self.assertEqual(visitor_mail.to, ["visitor@example.com"])
        self.assertIn("Thank you for contacting me", visitor_mail.subject)
        saved = ContactMessage.objects.get()
        self.assertTrue(saved.admin_mail_sent and saved.user_mail_sent)

    def test_invalid_email_is_rejected(self):
        data = dict(self.payload, email="not-an-email")
        self.client.post(reverse("send_contact_message"), data)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_same_email_twice_in_24_hours_is_blocked(self):
        self.client.post(reverse("send_contact_message"), self.payload)
        self.client.post(reverse("send_contact_message"), self.payload)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 2)

    def test_honeypot_blocks_bots(self):
        data = dict(self.payload, website="http://spam.example")
        self.client.post(reverse("send_contact_message"), data)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_get_is_not_allowed(self):
        response = self.client.get(reverse("send_contact_message"))
        self.assertEqual(response.status_code, 405)
