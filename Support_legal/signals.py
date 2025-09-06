from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Feedback, Testimonial
from ai_utils import analyze_sentiment

@receiver(pre_save, sender=Feedback)
def update_feedback_sentiment(sender, instance, **kwargs):
    instance.ai_sentiment = analyze_sentiment(instance.detailed_feedback)

@receiver(pre_save, sender=Testimonial)
def update_testimonial_sentiment(sender, instance, **kwargs):
    instance.ai_sentiment = analyze_sentiment(instance.content)
