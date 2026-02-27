import csv
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from image_analysis import detect_color
from csv_search import load_clothes, find_by_color, find_best_matches

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_ml_predictions(image_path):
    """Get ML-based predictions (lazy load to avoid slow startup)"""
    try:
        from ml_model import predict_image, map_to_category
        predictions = predict_image(image_path)
        category = map_to_category(predictions)
        return {
            "predictions": [(label, float(score)) for _, label, score in predictions],
            "category": category
        }
    except Exception as e:
        print(f"ML prediction error: {e}")
        return {"predictions": [], "category": "unknown"}


def get_similar_images(image_path):
    """Find similar images (lazy load)"""
    try:
        from image_similarity import find_similar_images, load_features
        features = load_features()
        if features:
            return find_similar_images(image_path, features, top_n=3)
        return []
    except Exception as e:
        print(f"Similarity error: {e}")
        return []


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    filename = None
    error = None

    if request.method == "POST":
        file = request.files.get("photo")
        
        # Validate file
        if not file or not file.filename:
            error = "No file selected"
        elif not allowed_file(file.filename):
            error = f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        else:
            try:
                filename = secure_filename(file.filename)
                pathname = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(pathname)
                result = run_visual_search(pathname)
            except Exception as e:
                error = f"Error processing image: {str(e)}"
                print(f"Error: {e}")

    return render_template(
        "index.html",
        filename=filename,
        color=result["detected_color"] if result else None,
        pattern=result["detected_pattern"] if result else None,
        category=result["detected_category"] if result else None,
        ml_predictions=result["ml_predictions"] if result else None,
        matches=result["matches"] if result else None,
        similar_images=result["similar_images"] if result else None,
        error=error
    )


@app.route("/clothes")
def view_clothes():
    clothes = []
    categories = set()

    selected_category = request.args.get("category")

    with open("clothes.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            categories.add(row["category"])

            if not selected_category or row["category"] == selected_category:
                clothes.append(row)

    return render_template(
        "clothes.html",
        clothes=clothes,
        categories=sorted(categories),
        selected_category=selected_category,
    )


def run_visual_search(image_path):
    """Analyze image and find matching clothes"""
    # Color and pattern detection (existing)
    analysis = detect_color(image_path)
    color = analysis["color"]
    pattern = analysis["pattern"]
    
    # ML-based category detection (new from homework 11)
    ml_result = get_ml_predictions(image_path)
    category = ml_result["category"]
    ml_predictions = ml_result["predictions"]
    
    # Load clothes and find best matches with scoring (homework 12)
    clothes = load_clothes()
    matches = find_best_matches(clothes, color, category, pattern, top_n=5)
    
    # If no scored matches, fall back to color-only matches
    if not matches:
        matches = find_by_color(color, clothes)[:5]
    
    # Find similar images (homework 13)
    similar_images = get_similar_images(image_path)

    return {
        "detected_color": color,
        "detected_pattern": pattern,
        "detected_category": category,
        "ml_predictions": ml_predictions,
        "matches": matches,
        "similar_images": similar_images
    }


if __name__ == "__main__":
    print("Starting Clothing Recommender App...")
    print("Open http://localhost:5001 in your browser")
    app.run(debug=True, port=5001)