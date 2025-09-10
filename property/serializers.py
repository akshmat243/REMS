from rest_framework import serializers
from .models import (
    PropertyType, Address, Property, PropertyImage, 
    PropertyAmenity, PropertyDocument, PostedProperty
)
from django.contrib.auth import get_user_model


User = get_user_model()


# ---------------- PropertyType ---------------- #
class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = "__all__"


# ---------------- Address ---------------- #
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ["id", "image", "caption", "is_primary", "ai_tag", "uploaded_at"]


class PropertyAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAmenity
        fields = ["id", "amenity"]


class PropertyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDocument
        fields = ["id", "document_type", "document_file", "verified"]


class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # Nested read-only serializers
    images = PropertyImageSerializer(many=True, read_only=True)
    amenities = PropertyAmenitySerializer(many=True, read_only=True)
    documents = PropertyDocumentSerializer(many=True, read_only=True)

    # Write-only fields
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    images_caption = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    uploaded_documents = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    documents_type = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    amenities_list = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Property
        fields = "__all__"

    def create(self, validated_data):
        images = validated_data.pop("uploaded_images", [])
        captions = validated_data.pop("images_caption", [])
        documents = validated_data.pop("uploaded_documents", [])
        doc_types = validated_data.pop("documents_type", [])
        amenities = validated_data.pop("amenities_list", [])

        # Create property instance
        property_instance = Property.objects.create(**validated_data)

        # Save amenities
        for amenity in amenities:
            PropertyAmenity.objects.create(property=property_instance, amenity=amenity)

        # Save images
        for i, img in enumerate(images):
            PropertyImage.objects.create(
                property=property_instance,
                image=img,
                caption=captions[i] if i < len(captions) else "",
            )

        # Save documents
        for i, doc in enumerate(documents):
            PropertyDocument.objects.create(
                property=property_instance,
                document_file=doc,
                document_type=doc_types[i] if i < len(doc_types) else "Other",
            )

        # 🔑 Reload with related objects so they appear in response
        return Property.objects.prefetch_related("amenities", "images", "documents").get(
            id=property_instance.id
        )

# ---------------- PostedProperty ---------------- #
class PostedPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostedProperty
        fields = "__all__"
        read_only_fields = ["id", "posted_on", "slug"]
        