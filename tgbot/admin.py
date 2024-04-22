from django.contrib import admin
from tgbot.models import User as TelegramUser, Complaint, NecessaryLink, Referral


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


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ("id", "link", "link_count")

    def link_count(self, obj):
        return obj.user_set.count()
