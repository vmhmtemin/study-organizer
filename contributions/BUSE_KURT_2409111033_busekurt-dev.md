# Member 1
Name: Buse Kurt, 
Student ID: 2409111033,
GitHub username: busekurt-dev

## Priority
Developed a priority system that organizes study tasks based on difficulty, deadline urgency, and completion status.

### Key Features
* **Priority Scoring:** Calculates scores using task difficulty and deadline urgency.
* **Deadline Tracking:** Calculates remaining days and identifies overdue tasks.
* **Task Sorting:** Orders pending tasks by priority, followed by overdue and completed tasks.
* **Task Comparison:** Uses deadline proximity to break ties between tasks with equal scores.

### Concepts Used
* **Dictionaries:** Stores difficulty scores; `DIFFICULTY`
* **Functions:**  Divide the logic into reusable parts;`days_left()`, `get_score()`, `is_better()`, and `order_tasks()`
* **Conditional Statements:** `if`, `elif`, and `else`
* **Loops:** `for`categorize and compare tasks; a `while` builds the priority order.
* **Lists:** Store tasks according to their status; `waiting`, `late`, and `finished`
* **Date Handling:** `date.today()` and `date.fromisoformat()` calculate the time remaining until deadlines.
* **Comparison Logic and Manuel Sorting:** `is_better()` compares priority scores and deadlines to determine which task comes first.


## Command-Line Interface (CLI)
Developed a command-line interface that allows users to manage study tasks and access study materials through terminal commands.

### Key Features
* **Task Management:** Supports adding, listing, viewing details, and marking tasks as completed.
* **Argument Handling:** Accepts commands and options such as task titles, deadlines, difficulty levels, and course names.
* **Input Validation:** Checks task information and task numbers before processing commands.
* **Material Access:** Supports importing, listing, and opening study materials.
* **Data Persistence:** Saves task changes and loads existing tasks.

### Concepts Used
* **Modules and Imports:** Imports functions from `main`, `materials`, `priority`, `storage`, and `tasks`.
* **Functions:** `main()`, `get_task()`, and `add_command()` organize CLI operations.
* **`argparse`:** Defines commands and optional arguments using `ArgumentParser()` and `add_argument()`.
* **Conditional Statements:** `if`, `elif`, and `else`
* **Lists and Dictionaries:** Stores available commands; `COMMANDS`
* **Input Validation:** `check_task()`, `check_number()`, and `check_file()` validate user inputs.
* **File and Data Handling:** Support data storage and material access;`load_tasks()`, `save_tasks()`, and `open_file()`


## README and Testing
Contributed to preparing parts of the project's README documentation, including project information and usage instructions. Participated in testing the code to verify that the application's features worked as expected, identify potential errors, and observe unexpected behavior. Also supported the improvement of the application by helping identify issues during testing.


