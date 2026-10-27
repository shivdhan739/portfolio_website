from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("skills/", views.skills, name="skills"),
    path("projects/", views.projects, name="projects"),
    path("education/", views.education, name="education"),
    path("contact/", views.contact, name="contact"),
    path(
        "contact/send/",
        views.send_contact_message,
        name="send_contact_message",
    ),
]
