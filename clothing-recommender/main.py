from image_analysis import detect_color
from csv_search import load_clothes, find_by_color

IMAGE_PATH = "static/uploads/redDress.webp"

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
    result = run_visual_search(IMAGE_PATH)

    print(f"Detected color: {result['detected_color']}")
    print("Matches:")

    for item in result["matches"]:
        print(f"- {item['name']} ({item['brand']}) → {item['link']}")
