**Web Development Basics – Simple Web Interface**

**Goal:** At the end of this homework you should have built a **basic web interface** using **Flask** that allows users to:

  - Upload a clothing photo
  - View uploaded images
  - Display clothing data from a CSV file

This simulates the **frontend of the Clothing Recommender app**.


**Step-by-step tasks:**

1. **Flask Basics**:
   - Create the following project structure in your IDE. Initially the files should be empty and gradually in the next steps you will add content:
     ```
      app.py
      templates/
        index.html
        clothes.html
      static/
        uploads/
      ```

      <img width="386" height="242" alt="image" src="https://github.com/user-attachments/assets/3468f5b2-b664-4a48-9279-09831c0883a7" />

   - What Flask is (lightweight web framework)
       - install Flask via `pip install flask`
       - validate Flask is installed via `python -c "import flask; print(flask.__version__)"`
         
         <img width="970" height="83" alt="image" src="https://github.com/user-attachments/assets/369fcbae-4c59-464c-8288-c611818da4e4" />

       - Routes (`@app.route`)
       - Running a local web server
       
         Below you could find the content of `app.py`
         ```
          from flask import Flask

          app = Flask(__name__)
          
          
          @app.route("/")
          def home():
              return "Hello, Flask!"
          
          
          if __name__ == "__main__":
              app.run(debug=True)

         ```

         Now you can Run `app.py` from the IDE (or in the console via `python app.py`). <br>
         You should see something like: `Running on http://127.0.0.1:5000` <br>
         Open your browser and go to: `http://127.0.0.1:5000` <br>
         You should see: `Hello, Flask!` <br>
         🎉 Congratulations! Your Flask server is running locally. <br>

2. **HTML + Flask Templates**
    - Basic HTML structure
    - Flask templates with `Jinja ({{ }})`
    - Displaying variables in HTML
    - `url_for()` usage
      
      Open `templates/index.html` (our frontend) and insert the code below (implementing the above concepts):
    
        ```
        <!DOCTYPE html>
        <html>
        <head>
            <title>Clothing Photo Upload</title>
        </head>
        <body>
        
        <h1>Upload a Dress Photo</h1>
        
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="photo" accept="image/*" required>
            <button type="submit">Upload</button>
        </form>
        
        {% if filename %}
            <h2>Uploaded Image</h2>
            <p>🔍 Searching for matches...</p>
            <img src="{{ url_for('static', filename='uploads/' + filename) }}"
                 alt="Uploaded image"
                 width="300">
        {% endif %}
        
        </body>
        </html>
        ```
    - Forms & File Uploads
    - HTML `<form>`
    - `POST` vs `GET`
    - Uploading image files
    - Handling `request.files`
      
      Update `app.py` (our backend) as per the abovve concepts: open `app.py` and replace its contents with:
      ```
      import os
      from flask import Flask, render_template, request
      
      app = Flask(__name__)
      
      # Folder where uploaded images will be saved
      UPLOAD_FOLDER = "static/uploads"
      app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
      
      
      @app.route("/", methods=["GET", "POST"])
      def home():
          filename = None
      
          if request.method == "POST":
              file = request.files.get("photo")
      
              if file and file.filename != "":
                  file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                  file.save(file_path)
                  filename = file.filename
      
          return render_template("index.html", filename=filename)
      
      
      if __name__ == "__main__":
          app.run(debug=True)

      ```

       Now you can Stop and Run again the `app.py` from the IDE (or in the console via `python app.py`). <br>
       You should see something like: `Running on http://127.0.0.1:5000` <br>
       Open your browser and go to: `http://127.0.0.1:5000` <br>
       You should see: <br>
       <img width="559" height="258" alt="image" src="https://github.com/user-attachments/assets/e843f2eb-2ae3-4047-a1d3-cb4c082eb31a" />
       <br> Now you can choose an image with a cloth and then click `Upload`. <br>
       You should see the same image in the browser and also it should be stored under `static/uploads`: <br>
       <img width="415" height="332" alt="image" src="https://github.com/user-attachments/assets/c909f8ed-6915-4941-824a-318b00401605" />
       <br>Now try to understand what just happened and how this worked. Upload some more clothes to the backend.

**Resources**
  - Flask Quickstart (official docs)
  - Corey Schafer – Flask playlist (YouTube)
  - W3Schools – HTML forms & file input


---
**HOMEWORK**
  - **Task 1**: Display Clothing from CSV <br>
    Add a new route `/clothes` that:<br>
    - Reads data from clothes.csv
    - Displays clothing items in an HTML table or list
    - Shows:
      - Name
      - Brand
      - Price
      - Category

  - **Task 2**: Navigation
    Add a navigation menu visible on all pages: <br>
    - “Upload Photo” -> `/` <br>
    - “View Clothes” -> `clothes` <br>
    - Filter by Category: Add a dropdown to filter clothes by category. <br>
    **Hints**: Create a Base Template with Navigation (`templates/base.html`). <br>
    Update the Upload Page (`templates/index.html`) to Use Navigation (`base.html`). <br>
    Add the “View Clothes” Page (it should also use `base.html`). <br>
    Add the `/clothes` route in `app.py`. <br>
    Now the Project Structure should look like: <br>
      ```
      flask_clothing_app/
      │
      ├── app.py
      ├── clothes.csv
      ├── templates/
      │   ├── base.html
      │   ├── index.html
      │   └── clothes.html
      └── static/
          └── uploads/
      ```
---
- (Optional): [OpenCode](https://opencode.ai/) - think how we could use it for our project?
