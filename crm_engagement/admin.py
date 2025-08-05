from django.contrib import admin
from .models import Lead, InteractionLog, Notification, Wishlist, PropertyComparison

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
