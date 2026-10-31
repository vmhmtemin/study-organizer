# storage.py - saves tasks to tasks.txt and loads them back
# File format: one task per line, fields separated by "|"
#   Lab 2|python|2026-12-18|hard|False|week2.pdf
from tasks import new_task, check_task


def save_tasks(tasks, filename="tasks.txt"):
    # Writes the task list to a file. "w" mode erases the old content and starts fresh.
    with open(filename, "w", encoding="utf-8") as file:
        for task in tasks:
            # Put each task's fields in a list in a fixed order.
            # "done" is a bool, so we convert it to text with str().
            fields = [task["title"], task["course"], task["deadline"],
                      task["difficulty"], str(task["done"]), task["file"]]
            # Join the fields with "|" and write them as a single line
            file.write("|".join(fields) + "\n")


def load_tasks(filename="tasks.txt"):
    # Reads the tasks from a file and returns them as a list of dictionaries.
    tasks = []
    skipped = 0  # number of damaged lines

    try:
        with open(filename, encoding="utf-8") as file:
            for line in file:
                # Strip the trailing whitespace/newline, then split into fields on "|"
                parts = line.strip().split("|")

                # Apply the same checks as for typed input:
                # there must be exactly 6 fields, and the title/course/deadline/difficulty must be valid.
                # check_task returns an empty string ("") when everything is valid.
                if len(parts) == 6 and check_task(parts[0], parts[1], parts[2], parts[3]) == "":
                    task = new_task(parts[0], parts[1], parts[2], parts[3], parts[5])
                    # new_task sets "done" on its own, so we convert the value
                    # from the file (the text "True"/"False") to a bool and overwrite it
                    task["done"] = parts[4] == "True"
                    tasks.append(task)
                elif line.strip() != "":
                    # Damaged but non-empty line: skip it instead of using it, and count it.
                    # (Completely blank lines are not counted.)
                    skipped += 1
    except FileNotFoundError:
        pass  # first run: there is no file yet, so we return an empty list

    # If any lines were skipped, warn the user
    if skipped > 0:
        print(f"Warning: {skipped} damaged line(s) in {filename} were skipped.")
    return tasks


def task_key(task):
    """One text that identifies a task. A new deadline gives a new key, so it is reminded again."""
    return "|".join([task["title"], task["course"], task["deadline"]])


def save_reminded(keys, filename="reminded.txt"):
    # One key per line: the tasks we already reminded the student about.
    with open(filename, "w", encoding="utf-8") as file:
        for key in keys:
            file.write(key + "\n")


def load_reminded(filename="reminded.txt"):
    keys = []
    try:
        with open(filename, encoding="utf-8") as file:
            for line in file:
                if line.strip() != "":
                    keys.append(line.strip())
    except FileNotFoundError:
        pass  # first run: nothing was reminded yet
    return keys


def save_deadlines(deadlines, filename="seen_deadlines.txt"):
    # One line per announcement: id|deadline
    with open(filename, "w", encoding="utf-8") as file:
        for record_id in deadlines:
            file.write(record_id + "|" + deadlines[record_id] + "\n")


def load_deadlines(filename="seen_deadlines.txt"):
    deadlines = {}
    try:
        with open(filename, encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 2:
                    deadlines[parts[0]] = parts[1]
    except FileNotFoundError:
        pass  # first scan: nothing is known yet
    return deadlines


# This block runs only when the file is executed directly
# (not when it is imported from another file). It is meant as a quick test.
if __name__ == "__main__":
    # Use a separate test file so the real tasks.txt is not touched
    save_tasks([new_task("Test", "dsa", "2100-01-01", "easy", "")], "test_tasks.txt")
    print(load_tasks("test_tasks.txt"))
  

    