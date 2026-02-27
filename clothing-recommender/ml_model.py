import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
import os
import pickle

# Load model once at startup
model = MobileNetV2(weights="imagenet")

# Feature extraction model (without final classification layer)
feature_model = Model(inputs=model.input, outputs=model.layers[-2].output)


def predict_image(img_path):
    """Run MobileNetV2 prediction on an image"""
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    
    predictions = model.predict(img_array, verbose=0)
    decoded = decode_predictions(predictions, top=3)[0]
    
    return decoded


def map_to_category(predictions):
    """Map AI predictions to clothing categories"""
    category_keywords = {
        "dress": ["dress", "gown", "miniskirt"],
        "shirt": ["shirt", "jersey", "sweatshirt", "cardigan", "sweater", "polo"],
        "pants": ["jean", "pants", "trouser"],
        "jacket": ["jacket", "coat", "blazer", "suit"],
        "skirt": ["skirt", "miniskirt"],
        "shoes": ["shoe", "sneaker", "boot", "sandal", "loafer"],
        "bag": ["bag", "handbag", "purse", "backpack"],
        "hat": ["hat", "cap", "bonnet"],
    }
    
    for _, label, score in predictions:
        label_lower = label.lower()
        for category, keywords in category_keywords.items():
            if any(k in label_lower for k in keywords):
                return category
    
    return "unknown"


def extract_features(img_path):
    """Extract feature vector from an image for similarity comparison"""
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    
    features = feature_model.predict(img_array, verbose=0)
    return features.flatten()


def save_features(features_dict, filepath="image_features.pkl"):
    """Save extracted features to disk"""
    with open(filepath, "wb") as f:
        pickle.dump(features_dict, f)


def load_features(filepath="image_features.pkl"):
    """Load extracted features from disk"""
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            return pickle.load(f)
    return {}


if __name__ == "__main__":
    # Test with an uploaded image
    test_dir = "static/uploads"
    if os.path.exists(test_dir):
        for filename in sorted(os.listdir(test_dir)):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                filepath = os.path.join(test_dir, filename)
                print(f"\n{filename}:")
                
                # Get predictions
                results = predict_image(filepath)
                for r in results:
                    print(f"  {r[1]}: {r[2]:.2%}")
                
                # Map to category
                category = map_to_category(results)
                print(f"  Category: {category}")