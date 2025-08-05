from rest_framework import serializers
from .models import *
from django.utils.text import slugify
from ai_utils import analyze_sentiment
import uuid

class RequestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestInfo
        fields = '__all__'
        read_only_fields = ['slug']

    def create(self, validated_data):
        validated_data['slug'] = slugify(f"request-{uuid.uuid4()}")
        return super().create(validated_data)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['slug', 'ai_sentiment']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        validated_data['slug'] = slugify(f"feedback-{uuid.uuid4()}")
        validated_data['ai_sentiment'] = analyze_sentiment(validated_data['message'])
        return super().create(validated_data)


class ReportProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportProblem
        fields = '__all__'
        read_only_fields = ['slug']

    def create(self, validated_data):
        validated_data['slug'] = slugify(f"report-{uuid.uuid4()}")
        return super().create(validated_data)


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
        fields = '__all__'
        read_only_fields = ['slug', 'ai_priority']

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


class SummonsNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummonsNotice
        fields = '__all__'
        read_only_fields = ['slug']

    def create(self, validated_data):
        validated_data['slug'] = slugify(f"summons-{uuid.uuid4()}")
        return super().create(validated_data)


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
