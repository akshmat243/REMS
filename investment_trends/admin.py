from django.contrib import admin
from .models import PriceTrend, InvestmentOpportunity

@admin.register(PriceTrend)
class PriceTrendAdmin(admin.ModelAdmin):
    list_display = ['area', 'price_per_sqft', 'trend_date', 'market_indicator']
    list_filter = ['area', 'trend_date']
    search_fields = ['area', 'market_indicator']

@admin.register(InvestmentOpportunity)
class InvestmentOpportunityAdmin(admin.ModelAdmin):
    list_display = ['title', 'roi', 'risk_level']
    list_filter = ['risk_level']
    search_fields = ['title', 'description']
