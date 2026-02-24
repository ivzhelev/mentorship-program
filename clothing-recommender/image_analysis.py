from PIL import Image
from sklearn.cluster import KMeans
import numpy as np
import colorsys

IMAGE_SIZE = (100, 100)


def is_near_white(r, g, b, threshold=235):
    """Check if a color is near white (high brightness, low saturation)"""
    brightness = (r + g + b) / 3
    max_diff = max(abs(r - g), abs(g - b), abs(r - b))
    return brightness > threshold and max_diff < 25


def is_background_color(r, g, b):
    """
    Check if a color is likely a background (white, light gray, very light).
    More aggressive filtering than is_near_white.
    """
    brightness = (r + g + b) / 3
    max_diff = max(abs(r - g), abs(g - b), abs(r - b))
    
    # Pure white or near-white
    if brightness > 235 and max_diff < 30:
        return True
    
    # Light gray (high brightness, low color variance)
    if brightness > 200 and max_diff < 20:
        return True
    
    return False


def get_saturation(r, g, b):
    """Calculate saturation of an RGB color (0-1)"""
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    if max_c == 0:
        return 0
    return (max_c - min_c) / max_c


def get_non_background_pixels(image_path):
    """
    Get all non-background pixels from the image.
    Focus on center but expand if needed.
    Filters out white and light gray backgrounds.
    """
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img = img.resize(IMAGE_SIZE)
        
        width, height = img.size
        
        # Try center region first (40% of image)
        pixels = []
        margin_x = int(width * 0.3)
        margin_y = int(height * 0.3)
        
        for y in range(margin_y, height - margin_y):
            for x in range(margin_x, width - margin_x):
                r, g, b = img.getpixel((x, y))
                if not is_background_color(r, g, b):
                    pixels.append([r, g, b])
        
        # If center is mostly background, expand to larger area (60% of image)
        if len(pixels) < 50:
            pixels = []
            margin_x = int(width * 0.2)
            margin_y = int(height * 0.2)
            
            for y in range(margin_y, height - margin_y):
                for x in range(margin_x, width - margin_x):
                    r, g, b = img.getpixel((x, y))
                    if not is_background_color(r, g, b):
                        pixels.append([r, g, b])
        
        # If still mostly background, try entire image
        if len(pixels) < 50:
            pixels = []
            for y in range(height):
                for x in range(width):
                    r, g, b = img.getpixel((x, y))
                    if not is_background_color(r, g, b):
                        pixels.append([r, g, b])
        
        return np.array(pixels) if pixels else None


def get_all_center_pixels(image_path):
    """Get all pixels from center of image (no filtering)"""
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img = img.resize(IMAGE_SIZE)
        
        width, height = img.size
        margin_x = int(width * 0.25)
        margin_y = int(height * 0.25)
        
        pixels = []
        for y in range(margin_y, height - margin_y):
            for x in range(margin_x, width - margin_x):
                r, g, b = img.getpixel((x, y))
                pixels.append([r, g, b])
        
        return np.array(pixels)


def get_dominant_color(image_path):
    """
    Find the most dominant non-background color in the image.
    Prefers saturated (colorful) clusters over gray/neutral ones.
    Falls back to analyzing all pixels if the garment might be white.
    """
    all_pixels = get_all_center_pixels(image_path)
    
    # Check for colored pixels (saturated, medium brightness)
    colored_pixels = []
    white_cream_pixels = []
    
    for p in all_pixels:
        r, g, b = p
        brightness = (r + g + b) / 3
        saturation = get_saturation(r, g, b)
        max_diff = max(abs(int(r) - int(g)), abs(int(g) - int(b)), abs(int(r) - int(b)))
        
        # Colored pixel (has significant saturation)
        if saturation > 0.2 and brightness > 30 and brightness < 230:
            colored_pixels.append(p)
        # White/cream pixel (very bright, low saturation)
        elif brightness > 210 and saturation < 0.12 and max_diff < 25:
            white_cream_pixels.append(p)
    
    colored_ratio = len(colored_pixels) / len(all_pixels)
    white_ratio = len(white_cream_pixels) / len(all_pixels)
    
    # Only classify as white if:
    # 1. There's a significant white region (>20%)
    # 2. AND white pixels are more than colored pixels (white garment, not colored on white bg)
    # 3. AND colored pixels aren't overwhelming (< 35%)
    if white_ratio > 0.20 and white_ratio >= colored_ratio and colored_ratio < 0.35:
        if white_cream_pixels:
            avg = np.mean(white_cream_pixels, axis=0).astype(int)
            return tuple(avg)
    
    # Normal processing for colored garments
    pixels = get_non_background_pixels(image_path)
    
    # If most pixels were filtered as background, the garment might actually be white/light
    filtered_ratio = len(pixels) / len(all_pixels) if pixels is not None and len(all_pixels) > 0 else 0
    
    if pixels is None or len(pixels) < 10 or filtered_ratio < 0.15:
        # Very few non-background pixels - garment is likely white/very light
        # Analyze all center pixels instead
        pixels = all_pixels
        
        # Check if the dominant color of all pixels is truly white/light
        n_colors = min(3, max(2, len(pixels) // 100))
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        centers = kmeans.cluster_centers_.astype(int)
        labels = kmeans.labels_
        counts = np.bincount(labels)
        
        # Get most common cluster
        most_common_idx = np.argmax(counts)
        r, g, b = centers[most_common_idx]
        brightness = (r + g + b) / 3
        
        # If most common is very light, it's a white garment
        if brightness > 200:
            return tuple(centers[most_common_idx])
    
    # Use K-means to find dominant color clusters
    n_colors = min(5, max(2, len(pixels) // 100))
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    # Get cluster centers and their counts
    centers = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    counts = np.bincount(labels)
    total_pixels = len(pixels)
    
    # Score each cluster: prefer colorful (saturated) clusters with reasonable count
    best_idx = 0
    best_score = -1
    
    for idx in range(len(centers)):
        r, g, b = centers[idx]
        saturation = get_saturation(r, g, b)
        brightness = (r + g + b) / 3
        count_ratio = counts[idx] / total_pixels
        
        # Skip very light/white clusters
        if is_background_color(r, g, b):
            continue
        
        # Score: combination of saturation and count
        # Higher saturation is better (clothing is usually colorful)
        # Count matters but saturated colors with smaller counts may still be the garment
        score = (saturation * 2 + 0.3) * (count_ratio + 0.1)
        
        # Bonus for medium brightness (not too dark, not too light)
        if 50 < brightness < 200:
            score *= 1.2
        
        if score > best_score:
            best_score = score
            best_idx = idx
    
    # If we found a good colorful cluster
    if best_score > 0:
        return tuple(centers[best_idx])
    
    # Fallback: return the most common non-background cluster
    sorted_indices = np.argsort(-counts)
    for idx in sorted_indices:
        r, g, b = centers[idx]
        if not is_background_color(r, g, b):
            return tuple(centers[idx])
    
    # Last resort: return the darkest one
    darkest_idx = 0
    darkest_brightness = 999
    for idx in range(len(centers)):
        brightness = sum(centers[idx]) / 3
        if brightness < darkest_brightness:
            darkest_brightness = brightness
            darkest_idx = idx
    
    return tuple(centers[darkest_idx])


def rgb_to_color_name(rgb):
    """
    Convert RGB to color name using HSV color space
    """
    r, g, b = [x / 255.0 for x in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    
    # Convert hue to degrees
    h = h * 360
    
    # Check for white (high brightness, low saturation)
    if v > 0.85 and s < 0.1:
        return "white"
    
    # Check for black (very low brightness)
    if v < 0.15:
        return "black"
    
    # Check for gray (low saturation)
    if s < 0.12:
        if v > 0.8:
            return "white"
        elif v < 0.3:
            return "black"
        return "gray"
    
    # Determine color by hue
    # Red: 0-15 and 345-360
    if h < 15 or h >= 345:
        if v < 0.3:
            return "black"
        if s < 0.4 and v < 0.5:
            return "brown"
        return "red"
    
    # Orange: 15-45
    if 15 <= h < 45:
        if v < 0.4:
            return "brown"
        return "orange"
    
    # Yellow: 45-70
    if 45 <= h < 70:
        return "yellow"
    
    # Green: 70-165
    if 70 <= h < 165:
        return "green"
    
    # Blue: 165-260
    if 165 <= h < 260:
        if v < 0.3:
            return "navy"
        return "blue"
    
    # Purple: 260-290
    if 260 <= h < 290:
        return "purple"
    
    # Pink/Magenta: 290-345
    if 290 <= h < 345:
        return "pink"
    
    return "gray"


def detect_pattern(image_path):
    """
    Improved pattern detection: solid or striped
    Uses both horizontal and vertical stripe detection
    """
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img = img.resize((100, 100))
        
        width, height = img.size
        margin = 20
        
        # Analyze center region
        center_pixels = []
        for y in range(margin, height - margin):
            row = []
            for x in range(margin, width - margin):
                r, g, b = img.getpixel((x, y))
                brightness = (r + g + b) / 3
                row.append(brightness)
            center_pixels.append(row)
        
        if len(center_pixels) < 10:
            return "solid"
        
        # Check for horizontal stripes (brightness variance across rows)
        row_avgs = [sum(row) / len(row) for row in center_pixels]
        row_variance = np.std(row_avgs)
        
        # Check for vertical stripes (brightness variance across columns)
        col_avgs = []
        for x in range(len(center_pixels[0])):
            col_sum = sum(row[x] for row in center_pixels)
            col_avgs.append(col_sum / len(center_pixels))
        col_variance = np.std(col_avgs)
        
        # Count direction changes (peaks and valleys)
        def count_changes(values, threshold=5):
            changes = 0
            for i in range(2, len(values) - 2):
                prev_avg = (values[i-2] + values[i-1]) / 2
                next_avg = (values[i+1] + values[i+2]) / 2
                curr = values[i]
                
                # Is this a peak or valley?
                if (curr > prev_avg + threshold and curr > next_avg + threshold) or \
                   (curr < prev_avg - threshold and curr < next_avg - threshold):
                    changes += 1
            return changes
        
        h_changes = count_changes(row_avgs)
        v_changes = count_changes(col_avgs)
        
        # Striped if significant variance AND multiple direction changes
        # Higher thresholds to avoid false positives from shadows/lighting
        high_variance = row_variance > 25 or col_variance > 25
        many_changes = h_changes >= 5 or v_changes >= 5
        
        # Need both variance AND direction changes for striped pattern
        is_striped = high_variance and many_changes
        
        return "striped" if is_striped else "solid"


def detect_color(image_path):
    """
    Main function: detect color and pattern
    """
    rgb = get_dominant_color(image_path)
    color = rgb_to_color_name(rgb)
    pattern = detect_pattern(image_path)
    
    return {
        "rgb": rgb,
        "color": color,
        "pattern": pattern
    }


if __name__ == "__main__":
    import os
    
    test_dir = "static/uploads"
    if os.path.exists(test_dir):
        for filename in sorted(os.listdir(test_dir)):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                filepath = os.path.join(test_dir, filename)
                result = detect_color(filepath)
                print(f"{filename}: {result['color']} {result['pattern']} RGB{result['rgb']}")