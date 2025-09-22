from django.contrib import admin
from .models import (
    Property, PropertyType, Address, PropertyImage,
    PropertyAmenity, PropertyDocument, PostedProperty, PropertyContact
)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'price', 'category', 'property_status', 'ai_price_estimate']
    list_filter = ['category', 'property_status', 'availability_status', 'property_type']
    search_fields = ['title', 'location', 'owner__email']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['house_no', 'area', 'city', 'state', 'country']
    search_fields = ['city', 'state', 'pincode']

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'caption', 'is_primary', 'ai_tag']
    search_fields = ['property__title']
    list_filter = ['is_primary']

@admin.register(PropertyAmenity)
class PropertyAmenityAdmin(admin.ModelAdmin):
    list_display = ['property', 'amenity']

@admin.register(PropertyDocument)
class PropertyDocumentAdmin(admin.ModelAdmin):
    list_display = ['property', 'document_type', 'verified', 'verified_by', 'verified_at']
    search_fields = ['property__title']
    list_filter = ['verified']

@admin.register(PostedProperty)
class PostedPropertyAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'status', 'posted_date']
    list_filter = ['status']
    search_fields = ['user__email', 'property__title']

@admin.register(PropertyContact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('owner_name', 'email', 'phone_number', 'property', 'is_active', 'created_at')
    search_fields = ('owner_name', 'email', 'phone_number', 'property__name')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'slug')