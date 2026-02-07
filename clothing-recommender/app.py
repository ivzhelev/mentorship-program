import csv
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from image_analysis import detect_color
from csv_search import load_clothes, find_by_color

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    filename = None

    if request.method == "POST":
        file = request.files.get("photo")
        if file and file.filename:
            filename = secure_filename(file.filename)
            pathname = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(pathname)
            result = run_visual_search(pathname)

    return render_template("index.html", filename=filename,color=result["detected_color"] if result else None, cloth=result["matches"][0] if result and result["matches"] else None)


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
    analysis = detect_color(image_path)
    color = analysis["color"]

    clothes = load_clothes()
    matches = find_by_color(color, clothes)

    return {
        "detected_color": color,
        "matches": matches
    }

if __name__ == "__main__":
    app.run(debug=True)
