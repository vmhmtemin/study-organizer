# cli.py - command line (argparse). Run: python cli.py <command> [options]
#
#   python cli.py add --title Lab 2 --course python --deadline 2026-12-18 --difficulty hard
#   python cli.py list
#   python cli.py details --number 1
import argparse

from main import run_menu
from materials import import_files, make_folders, show_file, show_materials
from priority import order_tasks
from storage import load_tasks, save_tasks
from tasks import (check_file, check_number, check_task, new_task,
                   show_details, show_tasks)

COMMANDS = ["add", "list", "details", "done", "delete", "open", "import", "materials", "menu"]


def get_task(tasks, text):
    """Finds the task with this list number. Prints a warning and gives None if it is wrong."""
    ordered = order_tasks(tasks)
    if len(ordered) == 0:
        print("Error: there are no tasks yet.")
        return None
    problem = check_number(text, 1, len(ordered))
    if problem != "":
        print("Error:", problem)
        return None
    return ordered[int(text) - 1]


def add_command(args, tasks):
    # nargs="+" gives a list of words, join() puts them back together: Lab 2
    title = ""
    if args.title:
        title = " ".join(args.title).strip()
    course = (args.course or "").strip().lower()
    deadline = (args.deadline or "").strip()
    difficulty = (args.difficulty or "").strip().lower()
    file = (args.file or "").strip()

    problem = check_task(title, course, deadline, difficulty)
    if problem == "" and course != "":
        problem = check_file(course, file)
    if problem != "":
        print("Error:", problem)
        return

    tasks.append(new_task(title, course, deadline, difficulty, file))
    save_tasks(tasks)
    print("Task added:", title)


def main():
    make_folders()

    parser = argparse.ArgumentParser(description="Study Organizer")
    parser.add_argument("command", choices=COMMANDS, help="what to do")
    parser.add_argument("--number", help="task number from 'list' (details, done, delete, open)")
    parser.add_argument("--title", nargs="+", help="task title, several words are fine (add)")
    parser.add_argument("--course", help="python, dsa or diffeq (add)")
    parser.add_argument("--deadline", help="YYYY-MM-DD, example 2026-12-18 (add)")
    parser.add_argument("--difficulty", help="easy, medium or hard (add)")
    parser.add_argument("--file", help="name of a file in materials/<course>/ (add, optional)")
    args = parser.parse_args()

    tasks = load_tasks()

    if args.command == "menu":
        run_menu(tasks)
    elif args.command == "add":
        add_command(args, tasks)
    elif args.command == "list":
        show_tasks(order_tasks(tasks))
    elif args.command == "import":
        import_files()
    elif args.command == "materials":
        show_materials()
    else:
        # details, done and open all need a task number
        task = get_task(tasks, (args.number or "").strip())
        if task is None:
            return
        if args.command == "details":
            show_details(task)
        elif args.command == "done":
            task["done"] = True
            save_tasks(tasks)
            print("Done:", task["title"])
            
        elif args.command == "delete":
            answer = input(
                f"Delete '{task['title']}'? (y/n): "
            ).strip().lower()

            if answer == "y":
                tasks.remove(task)
                save_tasks(tasks)
                print("Task deleted.")
            else:
                print("Deletion cancelled.")

        elif task["file"] == "":
            print("Error: this task has no file.")
        else:
            show_file(task["course"], task["file"])


if __name__ == "__main__":
    main()
