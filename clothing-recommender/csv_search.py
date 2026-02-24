import csv

def load_clothes(csv_path="clothes.csv"):
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def find_by_color(color, clothes):
    """
    Filter clothes by detected color - searches the 'color' column
    """
    return [item for item in clothes if item.get("color", "").lower() == color.lower()]


if __name__ == "__main__":
    clothes = load_clothes()
    
    # Test with different colors
    for test_color in ["blue", "red", "green", "black"]:
        matches = find_by_color(test_color, clothes)
        print(f"\n{test_color.upper()} items ({len(matches)}):")
        for item in matches:
            print(f"  - {item['name']} ({item['price_bgn']} BGN)")