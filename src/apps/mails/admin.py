from django.contrib import admin

from src.apps.mails.models import Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("external_id", "user_id", "email", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("external_id", "user_id", "email", "subject")
    readonly_fields = ("created_at", "updated_at")
