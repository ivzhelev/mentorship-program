"""
Image Similarity Module
Uses feature extraction and cosine similarity to find visually similar items.
"""
import os
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


FEATURES_FILE = "image_features.pkl"


def save_features(features_dict, filepath=FEATURES_FILE):
    """Save extracted features to disk"""
    with open(filepath, "wb") as f:
        pickle.dump(features_dict, f)


def load_features(filepath=FEATURES_FILE):
    """Load extracted features from disk"""
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            return pickle.load(f)
    return {}


def add_image_features(image_path, item_id, features_dict=None):
    """
    Extract and store features for an image.
    Lazy import to avoid loading TensorFlow if not needed.
    """
    from ml_model import extract_features
    
    if features_dict is None:
        features_dict = load_features()
    
    features = extract_features(image_path)
    features_dict[item_id] = {
        "path": image_path,
        "features": features
    }
    
    save_features(features_dict)
    return features_dict


def find_similar_images(query_image_path, features_dict=None, top_n=3):
    """
    Find the most similar images to the query image.
    Returns list of (item_id, similarity_score) tuples.
    """
    from ml_model import extract_features
    
    if features_dict is None:
        features_dict = load_features()
    
    if not features_dict:
        return []
    
    # Extract features from query image
    query_features = extract_features(query_image_path)
    query_features = query_features.reshape(1, -1)
    
    # Calculate similarity with all stored images
    similarities = []
    for item_id, data in features_dict.items():
        stored_features = data["features"].reshape(1, -1)
        similarity = cosine_similarity(query_features, stored_features)[0][0]
        similarities.append({
            "item_id": item_id,
            "path": data["path"],
            "similarity": float(similarity)
        })
    
    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x["similarity"], reverse=True)
    
    return similarities[:top_n]


def build_features_from_uploads(uploads_dir="static/uploads"):
    """
    Build feature database from all images in uploads directory.
    """
    features_dict = {}
    
    if not os.path.exists(uploads_dir):
        return features_dict
    
    for filename in os.listdir(uploads_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            filepath = os.path.join(uploads_dir, filename)
            print(f"Extracting features from {filename}...")
            features_dict = add_image_features(filepath, filename, features_dict)
    
    return features_dict


if __name__ == "__main__":
    # Build features from existing uploads
    print("Building feature database...")
    features = build_features_from_uploads()
    print(f"Stored features for {len(features)} images")
    
    # Test similarity if we have images
    if len(features) >= 2:
        test_image = list(features.keys())[0]
        test_path = features[test_image]["path"]
        print(f"\nFinding similar images to {test_image}:")
        similar = find_similar_images(test_path, features)
        for item in similar:
            print(f"  {item['item_id']}: {item['similarity']:.2%}")