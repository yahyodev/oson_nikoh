from django.contrib import admin
from tgbot.models import User as TelegramUser, Complaint, NecessaryLink


@admin.register(TelegramUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "username", "telegram_id",)
    search_fields = ("full_name", "username", "telegram_id",)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(NecessaryLink)
class NecessaryLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "link", "title")
