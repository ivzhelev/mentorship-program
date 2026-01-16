**Python Basics – Getting Started with Fundamentals**

**Goal**: Build foundational skills for writing simple scripts.

**Topics**:

- Installing Python and an IDE (e.g. [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download) or [VS Code](https://code.visualstudio.com/)).
- [Variables](https://www.w3schools.com/python/python_variables.asp), [data types](https://www.w3schools.com/python/python_datatypes.asp) (strings, integers, lists, dictionaries),
  [basic operations](https://www.w3schools.com/python/python_operators.asp), [lists](https://www.w3schools.com/python/python_lists.asp)
- Control structures: [if-else](https://www.w3schools.com/python/python_conditions.asp), loops ([for](https://www.w3schools.com/python/python_for_loops.asp)/[while](https://www.w3schools.com/python/python_while_loops.asp)).
- [Functions](https://www.w3schools.com/python/python_functions.asp) and [modules](https://www.w3schools.com/python/python_modules.asp).
- [range](https://www.w3schools.com/python/python_range.asp), [arrays](https://www.w3schools.com/python/python_arrays.asp)
- Input/output: [Reading user input](https://www.w3schools.com/python/python_user_input.asp), [printing results](https://www.w3schools.com/python/python_output.asp).

**Additional Resources (Optional):**

- "Automate the Boring Stuff with Python" (free online book, chapters [1](https://automatetheboringstuff.com/3e/chapter1.html)-[6](https://automatetheboringstuff.com/3e/chapter6.html)).

**Homework**: 
1. Write a simple program **Size Converter:**
  - Read size in **cm**
  - Convert to **inches**
  - Handle invalid input
    
2. Mini-project: A text-based **Clothing Recommender**:
  - Use a [dictionary](https://www.w3schools.com/python/python_dictionaries.asp) to store a hardcoded list of Bulgarian brands like Teodor or Sinsay, for example:
    ```
    brands = {
      "Teodor": ["formal", "business"],
      "Sinsay": ["casual", "sport"]
    }
    ```
  - Ask for style
  - Use if/else to suggest a brand
  - Allow multiple attempts using a loop

    **Hint:** 
      ```
      while True:
        style = input("Enter clothing style (or 'exit' to quit): ").lower()
  
        if style == "exit":
          print("Goodbye!")
          break
  
        found = False
  
        for brand, styles in brands.items():
          if style in styles:
              print("Recommended brand:", brand)
              found = True
  
        if not found:
          print("Sorry, no brand found for this style.")
      ```
3. Create a **function** that: 
  - Accepts a dress description (e.g. "red floral")
  - Returns a mock store link, e.g. https://store.example.com/red-floral

4. (Optional) **Combined Mini-Project**
This version combines everything:
      ```
      def generate_store_link(description):
        return "https://store.example.com/" + description.replace(" ", "-").lower()


      brands = {
          "Teodor": ["formal", "business"],
          "Sinsay": ["casual", "sport"]
      }

      style = input("Choose a style: ").lower()
      color = input("Choose a color: ").lower()
      
      for brand, styles in brands.items():
          if style in styles:
              description = color + " " + style
              print("Recommended brand:", brand)
              print("Product link:", generate_store_link(description))
      ```

  5. (Optional) Check the ideas to be implemented here: https://trello.com/b/9qIfYKFU/it-ideas-board  
