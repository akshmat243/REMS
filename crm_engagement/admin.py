from django.contrib import admin
from .models import Lead, InteractionLog, Notification, Wishlist, PropertyComparison, AgentProfile, AgentReview

@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user", "specialization", "experience_years", "deals_closed",
        "rating", "total_reviews", "verified", "slug"
    )
    list_filter = ("verified", "specialization", "experience_years")
    search_fields = ("user__full_name", "user__email", "specialization", "slug")
    prepopulated_fields = {"slug": ("user",)}  # optional, since slug is auto
    ordering = ("-rating", "-deals_closed")


@admin.register(AgentReview)
class AgentReviewAdmin(admin.ModelAdmin):
    list_display = ("agent", "user", "rating", "comment", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("agent__user__full_name", "user__full_name", "comment")
    readonly_fields = ("created_at",)

    def save_model(self, request, obj, form, change):
        """
        Ensures agent ratings update when reviews are created/edited in admin.
        """
        super().save_model(request, obj, form, change)
        obj.agent.update_rating_and_reviews()
        
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'interested_in', 'status']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['status']

@admin.register(InteractionLog)
class InteractionLogAdmin(admin.ModelAdmin):
    list_display = ['lead', 'interaction_type', 'date']
    search_fields = ['lead__name', 'notes']
    list_filter = ['interaction_type']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read']
    list_filter = ['is_read']
    search_fields = ['user__full_name', 'message']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'added_at']
    search_fields = ['user__full_name', 'property__title']
    list_filter = ['added_at']

@admin.register(PropertyComparison)
class PropertyComparisonAdmin(admin.ModelAdmin):
    list_display = ['user', 'property_1', 'property_2', 'compared_at']
    search_fields = ['user__full_name', 'property_1__title', 'property_2__title']
    list_filter = ['compared_at']
