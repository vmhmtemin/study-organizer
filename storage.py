# storage.py - save and load tasks.txt (one task per line, fields split by "|")
#   Lab 2|python|2026-12-18|hard|False|week2.pdf
from tasks import new_task, check_task


def save_tasks(tasks, filename="tasks.txt"):
    with open(filename, "w", encoding="utf-8") as file:     # "w" replaces the old content
        for task in tasks:
            fields = [task["title"], task["course"], task["deadline"],
                      task["difficulty"], str(task["done"]), task["file"]]
            file.write("|".join(fields) + "\n")


def load_tasks(filename="tasks.txt"):
    tasks = []
    skipped = 0
    try:
        with open(filename, encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                # the same checks as for typed input: a damaged line is skipped, not used
                if len(parts) == 6 and check_task(parts[0], parts[1], parts[2], parts[3]) == "":
                    task = new_task(parts[0], parts[1], parts[2], parts[3], parts[5])
                    task["done"] = parts[4] == "True"
                    tasks.append(task)
                elif line.strip() != "":
                    skipped += 1
    except FileNotFoundError:
        pass                          # first run: there is no file yet
    if skipped > 0:
        print(f"Warning: {skipped} damaged line(s) in {filename} were skipped.")
    return tasks


if __name__ == "__main__":
    save_tasks([new_task("Test", "dsa", "2100-01-01", "easy", "")], "test_tasks.txt")
    print(load_tasks("test_tasks.txt"))
