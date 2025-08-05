from rest_framework import serializers
from .models import *
from django.utils.text import slugify
import uuid

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = ['slug']

    def validate_phone(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits.")
        return value

    def create(self, validated_data):
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(f"lead-{uuid.uuid4()}")
        return super().create(validated_data)


class InteractionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractionLog
        fields = '__all__'
        read_only_fields = ['slug']

    def create(self, validated_data):
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(f"interaction-{uuid.uuid4()}")
        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['slug']

    def create(self, validated_data):
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(f"notification-{uuid.uuid4()}")
        return super().create(validated_data)


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'
        read_only_fields = ['slug']

    def create(self, validated_data):
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(f"wishlist-{uuid.uuid4()}")
        return super().create(validated_data)


class PropertyComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyComparison
        fields = '__all__'
        read_only_fields = ['slug']

    def validate(self, data):
        if data['property_1'] == data['property_2']:
            raise serializers.ValidationError("Cannot compare a property with itself.")
        return data

    def create(self, validated_data):
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(f"compare-{uuid.uuid4()}")
        return super().create(validated_data)
