# Week 11–14: Smart Recommendations & AI APIs

## Goal
Make your application smarter by improving recommendation logic and integrating external AI services.

---

# Part 1: Smart Recommendations

## Goal
Rank results instead of just filtering them.

---

## Task 1: Build a Scoring Function

```python
def score_item(item, detected_color, detected_category):
    score = 0

    if detected_color in item["color"]:
        score += 2

    if detected_category in item["name"].lower():
        score += 3

    return score
```

## Task 2: Sort Results

```python
items = load_clothes()

for item in items:
    item["score"] = score_item(item, color, category)

sorted_items = sorted(items, key=lambda x: x["score"], reverse=True)
```

## Task 3: Show Top Results

Display:

- Top 3 matches
- Include name, store, link

## Task 4

- Implement scoring system
- Sort results
- Show top 3 matches in UI

---

# Part 2: AI APIs

## Goal
Use external AI services instead of local models

---

## What You Will Learn
- What an API is
- Sending images to an API
- Parsing JSON responses

## Task 1: Choose an API

Options:
- OpenAI Vision
- Google Vision
- AWS Rekognition

## Task 2: Send an Image

- Upload image
- Send request to API
- Receive labels

## Task 3: Extract Useful Data

Example:
- "dress"
- "red"
- "floral"

## Task 4: Compare with Your Local Model 
- Which is more accurate?
- Which is faster?

## Task 5
- Integrate 1 AI API
- Extract labels
- Compare with MobileNet results and store the result of the comparison in a file
