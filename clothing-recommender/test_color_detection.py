#!/usr/bin/env python3
"""
Test color detection accuracy using filenames as ground truth.
Files with color names in their filename are used to validate the detection.
"""
import os
import re
from image_analysis import detect_color

UPLOAD_DIR = "static/uploads"

# Map filename patterns to expected colors
COLOR_PATTERNS = {
    "blue": "blue",
    "red": "red", 
    "orange": "orange",
    "black": "black",
    "white": "white",
    "green": "green",
    "yellow": "yellow",
    "pink": "pink",
    "purple": "purple",
    "gray": "gray",
    "grey": "gray",
    "brown": "brown",
    "navy": "blue",  # navy should be detected as blue
}


def extract_expected_color(filename):
    """
    Extract the expected color from filename.
    Returns None if no color found in filename.
    """
    filename_lower = filename.lower()
    
    for pattern, expected in COLOR_PATTERNS.items():
        # Look for color word in filename (not at word boundary to catch blueDress, redDress, etc.)
        if pattern in filename_lower:
            return expected
    
    return None


def run_tests():
    """
    Run color detection tests on all images with color names in filename.
    """
    if not os.path.exists(UPLOAD_DIR):
        print(f"Error: {UPLOAD_DIR} does not exist")
        return
    
    files = os.listdir(UPLOAD_DIR)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    
    # Collect test cases
    test_cases = []
    for filename in image_files:
        expected = extract_expected_color(filename)
        if expected:
            test_cases.append((filename, expected))
    
    if not test_cases:
        print("No test files found with color names in filename")
        return
    
    print("=" * 70)
    print("COLOR DETECTION VALIDATION TEST")
    print("=" * 70)
    print(f"\nTesting {len(test_cases)} images with color names in filename\n")
    
    passed = 0
    failed = 0
    results = []
    
    for filename, expected_color in test_cases:
        filepath = os.path.join(UPLOAD_DIR, filename)
        try:
            result = detect_color(filepath)
            detected_color = result["color"]
            rgb = result["rgb"]
            
            # Check if detected matches expected
            is_pass = detected_color == expected_color
            
            if is_pass:
                passed += 1
                status = "✓ PASS"
            else:
                failed += 1
                status = "✗ FAIL"
            
            results.append({
                "filename": filename,
                "expected": expected_color,
                "detected": detected_color,
                "rgb": rgb,
                "pass": is_pass
            })
            
        except Exception as e:
            failed += 1
            results.append({
                "filename": filename,
                "expected": expected_color,
                "detected": f"ERROR: {e}",
                "rgb": None,
                "pass": False
            })
    
    # Print results
    print("-" * 70)
    print(f"{'Filename':<45} {'Expected':<10} {'Detected':<10} {'Status'}")
    print("-" * 70)
    
    for r in results:
        short_name = r["filename"][-40:] if len(r["filename"]) > 40 else r["filename"]
        status = "✓ PASS" if r["pass"] else "✗ FAIL"
        print(f"{short_name:<45} {r['expected']:<10} {r['detected']:<10} {status}")
    
    print("-" * 70)
    print(f"\nRESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print(f"ACCURACY: {100 * passed / len(test_cases):.1f}%")
    print("=" * 70)
    
    # Print failed cases with RGB values for debugging
    if failed > 0:
        print("\nFAILED CASES DETAIL:")
        print("-" * 70)
        for r in results:
            if not r["pass"]:
                print(f"  File: {r['filename']}")
                print(f"    Expected: {r['expected']}, Detected: {r['detected']}")
                if r["rgb"]:
                    print(f"    RGB: {r['rgb']}")
                print()


if __name__ == "__main__":
    run_tests()