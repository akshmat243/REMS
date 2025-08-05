from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Property
from ai_utils import predict_property_price, calculate_recommendation_score

@receiver(pre_save, sender=Property)
def update_property_ai_fields(sender, instance, **kwargs):
    # Only update if needed, for example when the price or features change
    instance.ai_price_estimate = predict_property_price(instance)
    instance.ai_recommended_score = calculate_recommendation_score(instance)

from .models import PropertyImage
from ai_utils import classify_property_image

@receiver(pre_save, sender=PropertyImage)
def update_propertyimage_ai_tag(sender, instance, **kwargs):
    # Assuming instance.image.path contains the file path
    if instance.image and not instance.ai_tag:
        try:
            instance.ai_tag = classify_property_image(instance.image.path)
        except Exception:
            instance.ai_tag = ""

from .models import PropertyDocument
from ai_utils import extract_text_from_document

@receiver(pre_save, sender=PropertyDocument)
def update_document_ai_text(sender, instance, **kwargs):
    if instance.document_file and not instance.ai_extracted_text:
        try:
            instance.ai_extracted_text = extract_text_from_document(instance.document_file.path)
        except Exception:
            instance.ai_extracted_text = ""
