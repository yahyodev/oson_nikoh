from django.contrib import admin
from tgbot.models import User as TelegramUser, Complaint, NecessaryLink, Referral
from django.db.models import Count


@admin.register(TelegramUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location", "username", "telegram_id", 'status', 'complaint_count')
    search_fields = ("full_name", "username", "telegram_id", "location", "name")

    def get_queryset(self, request):
        # Prefetch the complaint count with each user to avoid N+1 queries problem
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _complaint_count=Count("accused")
        )
        return queryset

    def complaint_count(self, obj):
        # Utilize the annotated value for performance
        return obj._complaint_count

    complaint_count.admin_order_field = '_complaint_count'  # Allows column order sorting
    complaint_count.short_description = 'Complaints Received'  # Renames column head


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
