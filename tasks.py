# tasks.py - a task is a dictionary, plus the checks for what the user types
from datetime import date

from materials import COURSES, get_course_files
from priority import DIFFICULTY, days_left, get_score

BAD_TITLE_CHARACTERS = "|\t\r\n"        # "|" separates the fields in tasks.txt


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
        if character in title:
            return "Title cannot contain the character | or tabs."
    return ""


def check_choice(value, choices, name):
    """value must be one of the choices (a dictionary or a list)."""
    options = ", ".join(choices)
    if value == "":
        return f"{name.capitalize()} is required. Choose one of: {options}."
    if value not in choices:
        return f"'{value[:20]}' is not a valid {name}. Choose one of: {options}."
    return ""


def check_number(text, smallest, biggest):
    hint = f"Please enter a number from {smallest} to {biggest}."
    try:
        number = int(text)
    except ValueError:                  # the text is not a whole number
        return "Invalid number. " + hint
    if number < 0 and smallest >= 0:
        return "Negative numbers are not allowed. " + hint
    if number < smallest or number > biggest:
        return "Number out of range. " + hint
    return ""


def check_date(text):
    hint = "Use the format YYYY-MM-DD (year-month-day), for example 2026-12-18."
    if text == "":
        return "Deadline is required. " + hint
    if len(text) != 10 or text[4] != "-" or text[7] != "-":
        return "Invalid date. " + hint
    try:
        deadline = date.fromisoformat(text)     # fails for days that do not exist
    except ValueError:
        return "Invalid date. " + hint
    if deadline.year < 2000 or deadline.year > 2100:
        return "The year must be between 2000 and 2100."
    return ""


def check_file(course, filename):
    """The file name must be one of the files stored for the course ("" = no file)."""
    if filename == "" or filename in get_course_files(course):
        return ""
    return f"File '{filename[:30]}' was not found in materials/{course}/."


def check_task(title, course, deadline, difficulty):
    """Returns the first problem found, or "" if all values are fine."""
    problems = [
        check_title(title),
        check_choice(course, COURSES, "course"),
        check_date(deadline),
        check_choice(difficulty, DIFFICULTY, "difficulty"),
    ]
    for problem in problems:
        if problem != "":
            return problem
    return ""


# ---- showing tasks ----

def describe(task):
    if task["done"]:
        return "done"
    score = get_score(task)
    if score == "OVERDUE":
        return "OVERDUE"
    return f"score {score}, {days_left(task['deadline'])} days left"



def show_tasks(tasks):
    """Prints the numbered list of tasks."""
    print()
    print("========== YOUR TASKS ==========")

    if len(tasks) == 0:
        print("No tasks yet.")
        print("===============================")
        return

    number = 1
    for task in tasks:
        print()
        print(f"{number}. {task['title']}")
        print(f"   Course: {task['course']}")
        print(f"   Deadline: {task['deadline']}")
        print(f"   Difficulty: {task['difficulty']}")
        print(f"   Status: {describe(task)}")
        number += 1

    print()
    print("================================")



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


if __name__ == "__main__":
    print(check_date("2026-13-45"))
    print(check_number("-3", 1, 7))
    print(check_task("Lab 2", "math", "2100-01-01", "hard"))
