import random
from decimal import Decimal
from textblob import TextBlob
import pytesseract
from PIL import Image

def predict_property_price(property_instance):
    """
    Dummy price predictor: you can replace this with your ML model.
    For demonstration, we calculate a price that's 10% above the base price.
    """
    base_price = property_instance.price or Decimal("0.00")
    predicted_price = base_price * Decimal("1.10")
    return predicted_price.quantize(Decimal("0.01"))

def calculate_recommendation_score(property_instance):
    """
    Dummy recommendation score: returns a random float between 0 and 1.
    Replace this with a recommendation algorithm for production.
    """
    return round(random.uniform(0.0, 1.0), 2)

def analyze_sentiment(text):
    """
    Uses TextBlob to analyze sentiment.
    Returns "Positive", "Neutral", or "Negative".
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.3:
        return "Positive"
    elif polarity < -0.3:
        return "Negative"
    else:
        return "Neutral"

def classify_property_image(image_path):
    """
    Dummy image classifier: in production you might use a pre-trained CNN model
    or an API (like AWS Rekognition or Google Vision). Here, we return a random tag.
    """
    possible_tags = ["Bedroom", "Kitchen", "Living Room", "Bathroom", "Exterior"]
    return random.choice(possible_tags)

def extract_text_from_document(file_path):
    """
    Uses Tesseract OCR (via pytesseract) to extract text from an image/pdf.
    Assumes the file is an image file.
    """
    try:
        text = pytesseract.image_to_string(Image.open(file_path))
    except Exception:
        text = ""
    return text

# ai_utils.py

import openai
import os

# Set API key (ensure this is loaded from environment or settings)
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful real estate assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"[AI Error: {str(e)}]"

