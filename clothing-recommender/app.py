import csv
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def home():
    filename = None

    if request.method == "POST":
        file = request.files.get("photo")
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    return render_template("index.html", filename=filename)


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


if __name__ == "__main__":
    app.run(debug=True)
