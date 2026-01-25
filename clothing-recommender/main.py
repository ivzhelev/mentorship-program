import csv


def load_clothes(filename):
    clothes = []
    try:
        with open(filename, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["price_bgn"] = float(row["price_bgn"])
                clothes.append(row)
    except FileNotFoundError:
        print("Error: File not found.")
    except ValueError:
        print("Error: Invalid price in file.")
    return clothes


def search_by_price(items, max_price):
    return [item for item in items if item["price_bgn"] <= max_price]


def search_by_category(items, category):
    return [item for item in items if item["category"].lower() == category.lower()]


def print_items(items):
    if not items:
        print("No matching items found.")
    for item in items:
        print(
            f"✔ {item['name']} ({item['brand']}) – {item['price_bgn']} BGN"
        )


# ---- MAIN PROGRAM ----

clothes = load_clothes("clothes.csv")

if clothes:
    try:
        max_price = float(input("Enter maximum price (BGN): "))
        category = input("Enter category (e.g. dress, jacket): ")

        filtered = search_by_price(clothes, max_price)
        filtered = search_by_category(filtered, category)

        print("\nSearch results:")
        print_items(filtered)

    except ValueError:
        print("Please enter a valid number for price.")