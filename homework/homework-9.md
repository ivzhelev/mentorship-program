**Web Development Basics – Simple Web Interface**

**Goal:** Build a **basic web interface**00020 using **Flask** that allows users to:

  - Upload a clothing photo
  - View uploaded images
  - Display clothing data from a CSV file

This simulates the **frontend of the clothing recommender app**.

**Topics:**

1. **Flask Basics**:
    - [lists](https://www.w3schools.com/python/python_lists.asp) – store multiple clothing items
    - [dictionaries](https://www.w3schools.com/python/python_dictionaries.asp) – represent one product (name, brand, price, link)
    - [sets](https://www.w3schools.com/python/python_sets.asp) – keep unique values (e.g., brands, colors)

2. [File Handling (Persistent Data)](https://www.w3schools.com/python/python_file_handling.asp):
    - [Reading](https://www.w3schools.com/python/python_file_open.asp)/[writing](https://www.w3schools.com/python/python_file_write.asp) text files (e.g., CSV for store data).
    - Intro to Standard Libraries: import and use `csv`, [`json`](https://www.w3schools.com/python/python_json.asp).
      
3. [Basic error handling](https://www.w3schools.com/python/python_try_except.asp) (try-except).

**Resources:**

- Python.org documentation on built-in modules.
- Real Python tutorials on lists/dicts and file handling.
- Practice on LeetCode easy problems (e.g., array manipulation).

**Homework:**
1. **Task 1**: **Build a simple database:**

   Create a CSV file (a file called `clothes.csv`) with sample Bulgarian clothing items (with columns: name,brand,price_bgn,category,link). Add at least 10 items, for example:
    ```
      Red Summer Dress,Sinsay,79.99,dress,https://sinsay.com/red-dress
      Formal Jacket,Teodor,189.00,jacket,https://teodor.bg/jacket
    ```
2. **Task 2**: **Read & Search the CSV**

    Write a Python script that:

    1. Loads data from `clothes.csv`

    2. Asks the user for:

      - Maximum price

      - Category (e.g. dress, jacket)

    3. Displays matching items in a readable format

    Example output:
    ```
    Red Summer Dress (Sinsay) – 79.99 BGN
    ```

3. **Task 3**: **Functions & Error Handling**
   Create functions:
   ```
    load_clothes(filename)
    search_by_price(items, max_price)
    search_by_category(items, category)
   ```
   
   Use `try/except` to handle:
     - Missing file
     - Invalid user input

**Bonus (Optional)** Export to JSON

Save all matching search results into `results.json`

---
- (Optional): [OpenCode](https://opencode.ai/) - think how we could use it for our project?
