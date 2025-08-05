from rest_framework import serializers
from .models import PriceTrend, InvestmentOpportunity
from django.utils.text import slugify
import uuid
from datetime import date

class PriceTrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceTrend
        fields = '__all__'
        read_only_fields = ['slug']

    def validate_price_per_sqft(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price per sqft must be positive.")
        return value

    def validate_trend_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Trend date cannot be in the future.")
        return value

    def create(self, validated_data):
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(f"trend-{uuid.uuid4()}")
        return super().create(validated_data)


class InvestmentOpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentOpportunity
        fields = '__all__'
        read_only_fields = ['slug']

    def validate_roi(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("ROI must be between 0 and 100.")
        return value

    def create(self, validated_data):
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(f"opportunity-{uuid.uuid4()}")
        return super().create(validated_data)
