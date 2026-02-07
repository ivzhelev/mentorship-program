from PIL import Image
import os

# Resize for faster + more stable analysis
IMAGE_SIZE = (100, 100)

def get_average_color(image_path):
    """
    Returns average (R, G, B) tuple for an image
    """
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img = img.resize(IMAGE_SIZE)

        pixels = list(img.get_flattened_data())

        avg_r = sum(p[0] for p in pixels) // len(pixels)
        avg_g = sum(p[1] for p in pixels) // len(pixels)
        avg_b = sum(p[2] for p in pixels) // len(pixels)

        return avg_r, avg_g, avg_b


def rgb_to_color_name(r, g, b):
    """
    Map RGB values to human-readable color names
    """
    if r < 50 and g < 50 and b < 50:
        return "black"
    if r > 200 and g > 200 and b > 200:
        return "white"
    if r > 200 > g > 100 > b:
        return "orange"
    if r > g and r > b:
        return "red"
    if g > r and g > b:
        return "green"
    if b > r and b > g:
        return "blue"

    return "unknown"


def detect_color(image_path):
    r, g, b = get_average_color(image_path)
    color_name = rgb_to_color_name(r, g, b)

    return {
        "rgb": (r, g, b),
        "color": color_name
    }


if __name__ == "__main__":
    test_image = "static/uploads/blue2.png"
    result = detect_color(test_image)
    print(result)
