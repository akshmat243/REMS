from rest_framework import serializers
from .models import (
    PropertyType, Address, Property, PropertyImage, 
    PropertyAmenity, PropertyDocument, PostedProperty, PropertyContact as Contact
)
from django.contrib.auth import get_user_model


User = get_user_model()


class PropertyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "property",
            "owner_name",
            "email",
            "phone_number",
            "slug",
        ]
        read_only_fields = ["id", "slug", "property"]

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


# ---------------------------
# PropertyImageSerializer
# ---------------------------
class PropertyImageSerializer(serializers.ModelSerializer):
    # show property slug in responses
    property = serializers.SlugRelatedField(read_only=True, slug_field="slug")
    # accept slug on write & set the model FK (source='property')
    property_slug = serializers.SlugRelatedField(
        queryset=Property.objects.all(),
        slug_field="slug",
        source="property",
        write_only=True,
    )

    class Meta:
        model = PropertyImage
        fields = [
            "id",
            "property",       # read-only (slug shown)
            "property_slug",  # write-only input
            "image",
            "caption",
            "is_primary",
            "uploaded_at",
            "ai_tag",
            "slug",
        ]
        read_only_fields = ["id", "uploaded_at", "slug", "property"]

    def create(self, validated_data):
        # validated_data will already contain 'property' (the instance) because of SlugRelatedField
        return super().create(validated_data)


# ---------------------------
# PropertyAmenitySerializer
# ---------------------------
class PropertyAmenitySerializer(serializers.ModelSerializer):
    property = serializers.SlugRelatedField(read_only=True, slug_field="slug")
    property_slug = serializers.SlugRelatedField(
        queryset=Property.objects.all(),
        slug_field="slug",
        source="property",
        write_only=True,
    )

    class Meta:
        model = PropertyAmenity
        fields = ["id", "property", "property_slug", "amenity", "slug"]
        read_only_fields = ["id", "slug", "property"]

    def validate_amenity(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Amenity name must be at least 2 characters long.")
        return value

    def create(self, validated_data):
        return super().create(validated_data)


# ---------------------------
# PropertyDocumentSerializer
# ---------------------------
class PropertyDocumentSerializer(serializers.ModelSerializer):
    property = serializers.SlugRelatedField(read_only=True, slug_field="slug")
    property_slug = serializers.SlugRelatedField(
        queryset=Property.objects.all(),
        slug_field="slug",
        source="property",
        write_only=True,
    )
    document_file = serializers.FileField()

    class Meta:
        model = PropertyDocument
        fields = [
            "id",
            "property",
            "property_slug",
            "document_type",
            "document_file",
            "verified",
            "verified_by",
            "verified_at",
            "ai_extracted_text",
            "slug",
        ]
        read_only_fields = ["id", "slug", "verified_at", "ai_extracted_text", "property"]

    def validate_document_type(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("Document type must be at least 3 characters long.")
        return value

    def validate(self, data):
        # if verified True then verified_by must be present (business rule)
        if data.get("verified") and not data.get("verified_by"):
            raise serializers.ValidationError("Verified documents must have a verified_by user.")
        return data

    def create(self, validated_data):
        return super().create(validated_data)

class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # Nested read-only serializers
    images = PropertyImageSerializer(many=True, read_only=True)
    amenities = PropertyAmenitySerializer(many=True, read_only=True)
    documents = PropertyDocumentSerializer(many=True, read_only=True)
    contacts = PropertyContactSerializer(many=True, read_only=True)

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
    contact_owner_name = serializers.CharField(write_only=True, required=False)
    contact_email = serializers.EmailField(write_only=True, required=False)
    contact_phone_number = serializers.CharField(write_only=True, required=False)


    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ["id", "slug", "listed_on", "last_updated", "ai_price_estimate", "images", "amenities", "documents", "contacts"]

    def create(self, validated_data):
        images = validated_data.pop("uploaded_images", [])
        captions = validated_data.pop("images_caption", [])
        documents = validated_data.pop("uploaded_documents", [])
        doc_types = validated_data.pop("documents_type", [])
        amenities = validated_data.pop("amenities_list", [])
        owner_name = validated_data.pop("contact_owner_name", None)
        email = validated_data.pop("contact_email", None)
        phone = validated_data.pop("contact_phone_number", None)
        
        request = self.context.get("request")
        user = request.user if request else None

        location_str = validated_data.get("location", "")
        if location_str:
            parts = [p.strip() for p in location_str.split(",")]
            address_data = {
                "house_no": parts[0] if len(parts) > 0 else "",
                "street": parts[1] if len(parts) > 1 else "",
                "landmark": parts[2] if len(parts) > 2 else "",
                "area": parts[3] if len(parts) > 3 else "",
                "city": parts[4] if len(parts) > 4 else "",
                "state": parts[5] if len(parts) > 5 else "",
                "country": parts[6] if len(parts) > 6 else "",
                "pincode": parts[7].replace(" ", "") if len(parts) > 7 else "",
            }
            address = Address.objects.create(**address_data)
            validated_data["address"] = address
            
        # Decide property status
        validated_data["property_status"] = (
            "Active"
            if (user and (user.is_superuser or getattr(user, "role", None) in ["admin", "manager"]))
            else "Pending"
        )

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
        
        if owner_name or email or phone:
            Contact.objects.create(
                property=property_instance,
                owner_name=owner_name or "",
                email=email or "",
                phone_number=phone or "",
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
        