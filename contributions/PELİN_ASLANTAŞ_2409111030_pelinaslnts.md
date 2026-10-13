# Member 2
Name: Pelin Aslantaş
Student ID:  2409111030
GitHub username: pelinaslnts


## Storage
Developed the data storage module that saves and loads study tasks so that information is kept between sessions.

### Key Features
* **Data Persistence:** Saves task data to a file and loads it again when the program starts.
* **Task Creation:** Builds new task records with a title, course, difficulty, and deadline using `new_task()`.
* **Data Safety:** Checks stored and entered data before it is used by the rest of the application.

### Concepts Used
* **File Handling:** Reads from and writes to a file to store tasks permanently.
* **Dictionaries and Lists:** Represent each task as a dictionary and keep all tasks in a list.
* **Functions:** Split the logic into reusable parts such as `new_task()`, `describe()`, `show_tasks()`, and `show_details()`.
* **Conditional Statements:** `if`, `elif`, and `else`


## Input Validation and Task Display
Developed the validation functions that make sure user input is correct, and the functions that display tasks in the terminal.

### Key Features
* **Input Validation:** Checks titles, choices, numbers, dates, files, and task numbers before processing.
* **Error Prevention:** Rejects empty, invalid, or out-of-range input to avoid crashes.
* **Task Listing:** Shows all tasks in a readable list using `show_tasks()`.
* **Task Details:** Shows full information about a single task using `show_details()`.
* **Task Description:** Creates a short readable summary of a task using `describe()`.

### Concepts Used
* **Validation Functions:** `check_title()`, `check_choice()`, `check_number()`, `check_date()`, `check_file()`, and `check_task()`
* **Date Handling:** Validates deadline format with `date.fromisoformat()`.
* **Conditional Statements:** `if`, `elif`, and `else`
* **Loops:** `for` loops display tasks one by one.
* **String Formatting:** Formats task information for clear terminal output.
* **Exception Handling:** Catches invalid input (e.g., `ValueError`) instead of crashing.


## README
Contributed to preparing the project's README documentation, including project information, installation, and usage instructions.
