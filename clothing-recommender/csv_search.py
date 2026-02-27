import csv

def load_clothes(csv_path="clothes.csv"):
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def find_by_color(color, clothes):
    """
    Filter clothes by detected color - searches the 'color' column
    """
    return [item for item in clothes if item.get("color", "").lower() == color.lower()]


def score_item(item, detected_color, detected_category=None, detected_pattern=None):
    """
    Score an item based on how well it matches detected attributes.
    Higher score = better match.
    """
    score = 0
    
    # Color match (2 points for exact match, 1 for partial)
    item_color = item.get("color", "").lower()
    if detected_color and item_color:
        if detected_color.lower() == item_color:
            score += 2
        elif detected_color.lower() in item_color or item_color in detected_color.lower():
            score += 1
    
    # Category match (3 points)
    if detected_category and detected_category != "unknown":
        item_name = item.get("name", "").lower()
        item_category = item.get("category", "").lower()
        if detected_category.lower() in item_name or detected_category.lower() in item_category:
            score += 3
    
    # Pattern match (1 point)
    if detected_pattern:
        item_name = item.get("name", "").lower()
        if detected_pattern.lower() in item_name:
            score += 1
    
    return score


def find_best_matches(clothes, detected_color, detected_category=None, detected_pattern=None, top_n=3):
    """
    Find and rank the best matching items based on detected attributes.
    Returns top N matches sorted by score.
    """
    # Score all items
    scored_items = []
    for item in clothes:
        score = score_item(item, detected_color, detected_category, detected_pattern)
        item_with_score = item.copy()
        item_with_score["score"] = score
        scored_items.append(item_with_score)
    
    # Sort by score (highest first)
    sorted_items = sorted(scored_items, key=lambda x: x["score"], reverse=True)
    
    # Return top N with score > 0
    return [item for item in sorted_items[:top_n] if item["score"] > 0]


if __name__ == "__main__":
    clothes = load_clothes()
    
    # Test with different colors
    for test_color in ["blue", "red", "green", "black"]:
        matches = find_by_color(test_color, clothes)
        print(f"\n{test_color.upper()} items ({len(matches)}):")
        for item in matches:
            print(f"  - {item['name']} ({item['price_bgn']} BGN)")
    
    # Test scoring
    print("\n\nTesting scoring system:")
    best = find_best_matches(clothes, "blue", "shirt", "solid", top_n=5)
    print(f"Best matches for 'blue shirt solid':")
    for item in best:
        print(f"  - {item['name']} (score: {item['score']})")
