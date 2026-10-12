# tasks.py - Creates tasks, checks user inputs, and displays tasks
from datetime import date

# Import course information and priority functions from other files
from materials import COURSES, get_course_files
from priority import DIFFICULTY, days_left, get_score

# Characters that cannot be used in task titles
BAD_TITLE_CHARACTERS = "|\t\r"      # "|" separates the fields in tasks.txt

# Create a new task and store its information in a dictionary
def new_task(title, course, deadline, difficulty, file):
    """file = name of a file in materials/<course>/ ("" = no file)."""
    return {
        "title": title,
        "course": course,
        "deadline": deadline,       # text like "2026-12-18"
        "difficulty": difficulty,
        "done": False,
        "file": file,
    }


# ---- checks: each returns a warning text, or "" when everything is fine ----

def check_title(title):
    if title == "":
        return "Title cannot be empty."
    if len(title) > 40:
        return "Title is too long (maximum 40 characters)."
    for character in BAD_TITLE_CHARACTERS:
        if character in title:  # Check if the title contains this character
            return "Title cannot contain the character | or tabs."
    return ""

# Check if the user selected a valid option
def check_choice(value, choices, name):
    """value must be one of the choices (a dictionary or a list)."""
    options = ", ".join(choices) # Join all available choices into one string
    if value == "":
        return f"{name.capitalize()} is required. Choose one of: {options}."
    if value not in choices:
        return f"'{value[:20]}' is not a valid {name}. Choose one of: {options}."
    return ""

# Check if the input is a number within the allowed range
def check_number(text, smallest, biggest):
    hint = f"Please enter a number from {smallest} to {biggest}."
    try:
        number = int(text)  # Convert the input from string to integer
    except ValueError:                  # the text is not a whole number
        return "Invalid number. " + hint
    if number < 0 and smallest >= 0:
        return "Negative numbers are not allowed. " + hint
    if number < smallest or number > biggest:
        return "Number out of range. " + hint
    return ""

# Check if the deadline has a valid date format
def check_date(text):
    hint = "Use the format YYYY-MM-DD (year-month-day)"
    if text == "":
        return "Deadline is required. " + hint
    if len(text) != 10 or text[4] != "-" or text[7] != "-":  # Check the date format using string indexes
        return "Invalid date. " + hint
    try:
        deadline = date.fromisoformat(text)     # fails for days that do not exist
    except ValueError: # Handle invalid dates
        return "Invalid date. " + hint
    if deadline.year < 2000 or deadline.year > 2100:
        return "The year must be between 2000 and 2100."
    return ""

# Check if the selected file exists in the course folder
def check_file(course, filename):
    """The file name must be one of the files stored for the course ("" = no file)."""
    if filename == "" or filename in get_course_files(course): # Get the list of files belonging to the selected course
        return ""
    return f"File '{filename[:30]}' was not found in materials/{course}/."

# Check all important task information
def check_task(title, course, deadline, difficulty):
    """Returns the first problem found, or "" if all values are fine."""
    problems = [
        check_title(title),
        check_choice(course, COURSES, "course"),
        check_date(deadline),
        check_choice(difficulty, DIFFICULTY, "difficulty"),
    ]
    for problem in problems: # Check validation results one by one
        if problem != "":
            return problem
    return ""


# ---- showing tasks ----

def describe(task):
    if task["done"]:  # Access the completion status from the dictionary
        return "done"
    score = get_score(task) # Calculate the task priority score
    if score == "OVERDUE":
        return "OVERDUE"
    return f"score {score}, {days_left(task['deadline'])} days left"


# Display all tasks as a numbered list
def show_tasks(tasks):
    """Prints the numbered list of tasks."""
    print()
    print("========== YOUR TASKS ==========")

    if len(tasks) == 0:  # Check if the task list is empty
        print("No tasks yet.")
        print("===============================")
        return

    number = 1  # Start task numbering from 1
    for task in tasks: # Iterate through every task in the list
        print()
        print(f"{number}. {task['title']}") # Access the task title
        print(f"   Course: {task['course']}")
        print(f"   Deadline: {task['deadline']}")
        print(f"   Difficulty: {task['difficulty']}")
        print(f"   Status: {describe(task)}")
        number += 1 # Increase the task number by one

    print()
    print("================================")


# Display detailed information about one task
def show_details(task):
    print("\n" + task["title"])
    print("Course:", COURSES[task["course"]])
    print("Deadline:", task["deadline"])
    print("Difficulty:", task["difficulty"])
    print("Status:", describe(task))
    if task["file"] == "":
        print("File: none")
    else:
        print("File:", task["file"])

# Run these tests only when this file is executed directly
if __name__ == "__main__":
    print(check_date("2026-13-45"))
    print(check_number("-3", 1, 7))
    print(check_task("Lab 2", "math", "2100-01-01", "hard"))
