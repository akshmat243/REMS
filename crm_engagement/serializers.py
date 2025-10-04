from rest_framework import serializers
from .models import *
from django.utils.text import slugify
import uuid
from property.serializers import PropertySerializer

class AgentReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = AgentReview
        fields = ["id", "agent", "user_name", "rating", "comment", "created_at"]
        read_only_fields = ["id", "created_at", "user_name"]


class AgentReviewCreateSerializer(serializers.ModelSerializer):
    agent = serializers.SlugRelatedField(
        queryset = AgentProfile.objects.all(),
        slug_field="slug",
    )
    
    class Meta:
        model = AgentReview
        fields = ["agent", "rating", "comment"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)



class AgentProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    reviews = AgentReviewSerializer(many=True, read_only=True)

    class Meta:
        model = AgentProfile
        fields = [
            "id", "slug", "full_name", "specialization", "specialties", "languages",
            "experience_years", "properties_handled", "deals_closed",
            "rating", "total_reviews", "verified", "response_time",
            "profile_image", "phone", "email", "location", "about",
            "total_earnings", "reviews"
        ]
        read_only_fields = ["id", "slug", "rating", "total_reviews", "deals_closed", "reviews"]

    def get_recent_reviews(self, obj):
        reviews = obj.reviews.order_by("-created_at")[:5]
        return [
            {
                "user": r.user.full_name,
                "rating": r.rating,
                "comment": r.comment,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M"),
            }
            for r in reviews
        ]


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
    user = serializers.ReadOnlyField(source="user.email")
    property = PropertySerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(), 
        write_only=True, 
        source="property"
    )

    class Meta:
        model = Wishlist
        fields = ["slug", "user", "property", "property_id", "added_at"]
        read_only_fields = ["slug", "user", "added_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
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
