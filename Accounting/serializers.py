from rest_framework import serializers
from .models import *
from django.utils.text import slugify
import uuid
from decimal import Decimal

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['slug']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def create(self, validated_data):
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(f"txn-{uuid.uuid4()}")
        return super().create(validated_data)


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['slug']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Invoice amount must be positive.")
        return value

    def create(self, validated_data):
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(f"inv-{uuid.uuid4()}")
        return super().create(validated_data)


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'
        read_only_fields = ['slug']

    def create(self, validated_data):
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(f"rcpt-{uuid.uuid4()}")
        return super().create(validated_data)


class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = '__all__'
        read_only_fields = ['slug']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Commission must be a positive value.")
        return value

    def create(self, validated_data):
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(f"comm-{uuid.uuid4()}")
        return super().create(validated_data)
