from rest_framework import serializers
from .models import VisitRequest, Appointment, RentAgreement
from django.utils.text import slugify
import uuid

class VisitRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitRequest
        fields = '__all__'
        read_only_fields = ['slug', 'created_at']

    def validate_preferred_time(self, value):
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("Preferred time must be in the future.")
        return value

    def create(self, validated_data):
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(f"visit-{uuid.uuid4()}")
        return super().create(validated_data)


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['slug']

    def validate(self, data):
        if data['user'] == data['agent']:
            raise serializers.ValidationError("User and agent cannot be the same.")
        return data

    def create(self, validated_data):
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(f"appt-{uuid.uuid4()}")
        return super().create(validated_data)


class RentAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentAgreement
        fields = '__all__'
        read_only_fields = ['slug']

    def validate(self, data):
        if data['agreement_start'] >= data['agreement_end']:
            raise serializers.ValidationError("End date must be after start date.")
        return data

    def create(self, validated_data):
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(f"agreement-{uuid.uuid4()}")
        return super().create(validated_data)
