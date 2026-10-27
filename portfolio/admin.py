from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import ContactMessage, Project

admin.site.site_header = "Shivdhan Portfolio - Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Manage messages and projects"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read", "admin_mail_sent", "user_mail_sent", "reply")
    list_filter = ("is_read", "admin_mail_sent", "user_mail_sent", "created_at")
    list_editable = ("is_read",)
    search_fields = ("name", "email", "subject", "message")
    date_hierarchy = "created_at"
    readonly_fields = ("name", "email", "subject", "message", "ip_address", "created_at",
                       "admin_mail_sent", "user_mail_sent", "email_error", "reply")
    fields = readonly_fields + ("is_read",)
    actions = ["mark_read", "mark_unread"]

    def has_add_permission(self, request):
        return False  # messages come only from the website form

    @admin.display(description="Reply")
    def reply(self, obj):
        if not obj.pk:
            return "-"
        return format_html('<a href="mailto:{}?subject=Re: {}">Reply by email</a>', obj.email, obj.subject)

    @admin.action(description="Mark selected as read")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected as unread")
    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "order", "is_active", "link")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "tag")
    search_fields = ("title", "description", "tech")
