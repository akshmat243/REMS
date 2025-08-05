from django.contrib import admin
from .models import VisitRequest, Appointment, RentAgreement

@admin.register(VisitRequest)
class VisitRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'preferred_time', 'status', 'created_at']
    list_filter = ['status', 'preferred_time']
    search_fields = ['user__email', 'property__title']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'agent', 'appointment_time', 'status']
    list_filter = ['status']
    search_fields = ['user__email', 'agent__email']

@admin.register(RentAgreement)
class RentAgreementAdmin(admin.ModelAdmin):
    list_display = ['property', 'tenant', 'owner', 'monthly_rent', 'agreement_start', 'signed']
    list_filter = ['signed']
    search_fields = ['tenant__email', 'owner__email', 'property__title']
