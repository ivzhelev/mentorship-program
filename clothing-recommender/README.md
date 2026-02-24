# Clothing Recommender

A simple Flask app that detects the color of clothing from uploaded images and recommends matching items from a database.

## Features

- **Image Upload**: Upload a photo of clothing
- **Color Detection**: Automatically detects the dominant color (ignoring background)
- **Database Search**: Finds matching clothes by color
- **Browse Catalog**: View all available clothing items with filtering

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open http://localhost:5001 in your browser.

## How It Works

1. **Upload** a photo of clothing
2. The app **analyzes** the image to detect the dominant color
3. It **searches** the database for items matching that color
4. **Results** are displayed with links to view the items

## Color Detection

The app uses PIL (Pillow) to analyze images:
- Focuses on the center region where clothing typically is
- Filters out bright/white background pixels
- Uses HSV color space for accurate color naming
- Detects: red, orange, yellow, green, blue, purple, pink, black, white, gray

## Project Structure

```
clothing-recommender/
├── app.py              # Main Flask application
├── image_analysis.py   # Color detection logic
├── csv_search.py       # Database search functions
├── clothes.csv         # Clothing database
├── requirements.txt    # Dependencies
├── templates/
│   ├── base.html       # Base template
│   ├── index.html      # Upload page
│   └── clothes.html    # Browse page
└── static/
    └── uploads/        # Uploaded images
```

## Requirements

- Python 3.9+
- Flask
- Pillow