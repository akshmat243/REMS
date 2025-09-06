from rest_framework import serializers
from .models import *
from django.utils.text import slugify
from ai_utils import analyze_sentiment
import uuid

class RequestInfoSerializer(serializers.ModelSerializer):
    # Explicitly handle JSONField as ListField of strings
    info_types = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    class Meta:
        model = RequestInfo
        fields = "__all__"
        read_only_fields = ["id", "created_at"]

    def validate_info_types(self, value):
        """Ensure info_types only contain allowed choices"""
        valid_choices = [choice[0] for choice in RequestInfo.INFO_TYPES]
        for item in value:
            if item not in valid_choices:
                raise serializers.ValidationError(f"Invalid info_type: {item}")
        return value

class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = [
            "id",
            "user",
            "full_name",
            "email",
            "phone_number",
            "category",
            "priority",
            "subject",
            "message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            "id",
            "feedback_type",
            "rating",
            "name",
            "email",
            "subject",
            "category",
            "detailed_feedback",
            "what_went_well",
            "how_to_improve",
            "recommend_us",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        validated_data['slug'] = slugify(f"feedback-{uuid.uuid4()}")
        validated_data['ai_sentiment'] = analyze_sentiment(validated_data['message'])
        return super().create(validated_data)


class ProblemReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemReport
        fields = "__all__"
        read_only_fields = ("id", "created_at")


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'
        read_only_fields = ['slug', 'ai_sentiment']

    def create(self, validated_data):
        validated_data['slug'] = slugify(f"testimonial-{uuid.uuid4()}")
        validated_data['ai_sentiment'] = analyze_sentiment(validated_data['content'])
        return super().create(validated_data)


class GrievanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grievance
        fields = [
            "id",
            "user",
            "category",
            "priority",
            "title",
            "description",
            "property_id",
            "transaction_id",
            "evidence",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data['slug'] = slugify(f"grievance-{uuid.uuid4()}")
        # Reuse sentiment analysis for priority as a proxy
        sentiment = analyze_sentiment(validated_data['content'])
        validated_data['ai_priority'] = {
            'Positive': 'Low',
            'Neutral': 'Medium',
            'Negative': 'High'
        }.get(sentiment, 'Medium')
        return super().create(validated_data)


class CustomerServiceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerServiceLog
        fields = '__all__'
        read_only_fields = ['slug']

    def create(self, validated_data):
        validated_data['slug'] = slugify(f"service-{uuid.uuid4()}")
        return super().create(validated_data)


class NoticeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeResponse
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class ChatInteractionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatInteractionLog
        fields = '__all__'
        read_only_fields = ['slug', 'ai_response']

    def create(self, validated_data):
        validated_data['slug'] = slugify(f"chatlog-{uuid.uuid4()}")
        prompt = validated_data['query']
        validated_data['ai_response'] = ask_openai(prompt)
        return super().create(validated_data)
