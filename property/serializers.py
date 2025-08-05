from rest_framework import serializers
from .models import *
from django.utils.text import slugify
import uuid
from ai_utils import predict_property_price, calculate_recommendation_score, classify_property_image, extract_text_from_document

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'

    def validate_name(self, value):
        if PropertyType.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Property type already exists.")
        return value


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'
        read_only_fields = ['slug', 'ai_tag']

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image file too large (max 2MB).")
        return value

    def create(self, validated_data):
        validated_data['slug'] = slugify(f"propertyimage-{uuid.uuid4()}")
        instance = PropertyImage(**validated_data)
        if instance.image:
            validated_data['ai_tag'] = classify_property_image(instance.image.path)
        return super().create(validated_data)


class PropertyAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAmenity
        fields = '__all__'


class PropertyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDocument
        fields = '__all__'
        read_only_fields = ['slug', 'ai_extracted_text']

    def validate_document_file(self, value):
        if not value.name.endswith(('.pdf', '.docx')):
            raise serializers.ValidationError("Document must be a .pdf or .docx file.")
        return value

    def create(self, validated_data):
        validated_data['slug'] = slugify(f"propertydoc-{uuid.uuid4()}")
        instance = PropertyDocument(**validated_data)
        if instance.document_file:
            validated_data['ai_extracted_text'] = extract_text_from_document(instance.document_file.path)
        return super().create(validated_data)


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['slug', 'ai_price_estimate', 'ai_recommended_score']

    def validate_price(self, value):
        if value < 1000:
            raise serializers.ValidationError("Price must be greater than 1000.")
        return value

    def validate_area_sqft(self, value):
        if value <= 0:
            raise serializers.ValidationError("Area must be a positive number.")
        return value

    def create(self, validated_data):
        validated_data['slug'] = slugify(f"{validated_data.get('title')}-{uuid.uuid4()}")
        instance = Property(**validated_data)
        validated_data['ai_price_estimate'] = predict_property_price(instance)
        validated_data['ai_recommended_score'] = calculate_recommendation_score(instance)
        return super().create(validated_data)


class PostedPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostedProperty
        fields = '__all__'
