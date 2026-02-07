**Image Processing – Analyzing Photos**

**Goal:** 
Add a basic visual search engine:

  - Analyze an uploaded dress image
  - Guess **dominant color**
  - Guess **pattern type** (solid vs. striped)
  - Use that info to **filter clothing items from your CSV**

This is **not AI / ML yet** — just smart heuristics (perfect for learning).

**What we are building (mental model)**

```
  Image upload
     ↓
  Image analysis (Python)
     ↓
  Extract features:
     - dominant color
     - pattern type
     ↓
  Match against CSV
     ↓
  Show results in Flask

```

**Topics:**

**1. Installing image libraries**
    - `pip install pillow`
    - Optional later: `pip install opencv-python`

**2. Image basics (with Pillow)**
  You’ll learn to:
  
    - Load an image
    - Resize it (for faster processing)
    - Access pixels (RGB values)
  
  Key concepts:
  
    - Image size
    - RGB color model
    - Pixels as (R, G, B) tuples
        
**3. Color analysis (core skill)**
You’ll implement:

  - Average color detection
  - Mapping RGB → human labels (red, blue, black, etc.)

Example mapping logic:

```
  High R, low G/B → red
  Low all → black
  High all → white
```

**4. Pattern detection (simple but clever)**
No AI yet — just math.

You’ll detect:

- Solid → low pixel variation
- Striped → repeating horizontal/vertical color changes

Concepts:
- Pixel difference
- Variance
- Thresholds

**5. Feature extraction (very important concept)**
You’ll return structured data like:

```
  {
    "color": "red",
    "pattern": "striped"
  }
```
This prepares you for **machine learning later**.

**6. Flask integration**
After image upload:

 - Run image analysis
 - Match against CSV
 - Show result page

**Suggested folder structure (important)**

```
clothing-recommender/
│
├── app.py
├── image_analysis.py
├── clothes.csv
│
├── static/
│   └── uploads/
│
├── templates/
│   ├── index.html
│   └── results.html

```


---

**Homework:**
When Uploading a Dress Photo at at http://127.0.0.1:5000/, detect:   
1. **Dominant color detection** (almost implemented at https://github.com/ivzhelev/mentorship-program/tree/main/clothing-recommender)
  - Extract average RGB
  - Map to at least 5 colors:
    - red, blue, green, black, white

2. **CSV matching**
    - Add **color** and **pattern** columns to **clothes.csv**
    - Apart from the color detection, also detect the pattern of the uploaded dress photo. 
    - Using the detected color and pattern, display the closest matching Cloth Found from the **clothes.csv** (together with the link and the price of the cloth)

**Hint about pattern detection:**
- Convert image to grayscale
- Compare pixel differences row-by-row
- Rule:
  - Low variation → solid
  - High regular variation → striped
  Confidence message: `"This looks like a red striped dress (70% confidence)"`
