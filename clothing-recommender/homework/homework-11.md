# Week 9–10: ML-Based Image Recognition

## Goal
Upgrade your application from rule-based logic (color detection) to AI-powered image understanding using a pre-trained model.

---

## What You Will Learn
- What a pre-trained model is
- How to use an image classification model
- How to process images for ML
- How to interpret predictions

---

## Setup

Install required libraries:

```bash
pip install tensorflow pillow numpy
```

## Task 1: Run Your First AI Model

Create a file: `ml_model.py`

```
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

model = MobileNetV2(weights="imagenet")

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)

    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)
    decoded = decode_predictions(predictions, top=3)[0]

    return decoded

```

## Task 2: Print Predictions

```
results = predict_image("static/uploads/test.jpg")

for r in results:
    print(r)

```

Example output:

```
('n03534580', 'dress', 0.75)

```

## Task 3: Map AI → Clothing Category

Create a mapping function:

```
def map_to_category(predictions):
    keywords = ["dress", "gown", "skirt"]

    for _, label, score in predictions:
        if any(k in label.lower() for k in keywords):
            return "dress"

    return "unknown"

```

## Task 4: Integrate With Your Existing App

- Use uploaded image
- Run prediction
- Map result to category
- Print or display it in UI

## Taks 5

- Run MobileNet on an uploaded image
- Print top 3 predictions
- Map to category (dress/shirt/etc.)
- Combine:
    - detected color (previous weeks)
    - detected category (ML) <br>
  Example: `red dress`


