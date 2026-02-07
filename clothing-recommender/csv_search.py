import csv

def load_clothes(csv_path="clothes.csv"):
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def find_by_color(color, clothes):
    """
    Filter clothes by detected color
    """
    return [item for item in clothes if color.lower() in item["name"].lower()]


if __name__ == "__main__":
    clothes = load_clothes()
    matches = find_by_color("blue", clothes)

    for item in matches:
        print(f"{item['name']} - {item['link']} ({item['price_bgn']} BGN)")
