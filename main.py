# main.py - the menu (run it with: python main.py)
from materials import (COURSES, get_course_files, import_files,
                       make_folders, open_file, show_materials)
from priority import DIFFICULTY, order_tasks
from storage import load_tasks, save_tasks
from tasks import (check_choice, check_date, check_number, check_title,
                   new_task, show_details, show_tasks)

MENU = [
    "1. Add task",
    "2. Show tasks",
    "3. Task details / open file",
    "4. Mark task as done",
    "5. Import files from inbox",
    "6. Show materials",
    "7. Delete task",
    "0. Save and exit",
]


# ---- keep asking until the answer is fine ----

def ask_title(question):
    while True:
        answer = input(question).strip()          # strip(): remove spaces at both ends
        problem = check_title(answer)
        if problem == "":
            return answer
        print("  Warning:", problem)


def ask_choice(question, choices, name):
    while True:
        answer = input(question).strip().lower()  # lower(): "Python" is accepted as "python"
        problem = check_choice(answer, choices, name)
        if problem == "":
            return answer
        print("  Warning:", problem)


def ask_date(question):
    while True:
        answer = input(question).strip()
        problem = check_date(answer)
        if problem == "":
            return answer
        print("  Warning:", problem)


def ask_number(question, smallest, biggest):
    while True:
        answer = input(question).strip()
        problem = check_number(answer, smallest, biggest)
        if problem == "":
            return int(answer)
        print("  Warning:", problem)


# ---- menu actions ----

def pick_task(tasks):
    """Shows the list and lets the user choose a task (None if there are no tasks)."""
    ordered = order_tasks(tasks)
    if len(ordered) == 0:
        print("No tasks yet.")
        return None
    show_tasks(ordered)
    number = ask_number("Task number: ", 1, len(ordered))
    return ordered[number - 1]



def add_task(tasks):
    print()
    print("==============================")
    print("        ADD A NEW TASK")
    print("==============================")

    title = ask_title("Task title: ")
    course = ask_choice(f"Course ({', '.join(COURSES)}): ", COURSES, "course")
    deadline = ask_date("Deadline (YYYY-MM-DD, example 2026-12-18): ")
    difficulty = ask_choice(f"Difficulty ({', '.join(DIFFICULTY)}): ", DIFFICULTY, "difficulty")

    # Optional: choose a file for this course
    chosen_file = ""
    files = get_course_files(course)

    if len(files) > 0:
        for i in range(len(files)):
            print(f"{i + 1}. {files[i]}")

        number = ask_number("File number (0 = no file): ", 0, len(files))

        if number > 0:
            chosen_file = files[number - 1]

    tasks.append(new_task(title, course, deadline, difficulty, chosen_file))
    print("Task added!")



def show_task_details(tasks):
    task = pick_task(tasks)
    if task is not None:
        show_details(task)
        if task["file"] != "":
            answer = ask_choice("Open the file? (y/n): ", ["y", "n"], "answer")
            if answer == "y":
                open_file(task["course"], task["file"])


def mark_done(tasks):
    task = pick_task(tasks)
    if task is not None:
        task["done"] = True
        print("Done:", task["title"])


        
def delete_task(tasks):
    task = pick_task(tasks)

    if task is not None:
        answer = ask_choice(
            f"Delete '{task['title']}'? (y/n): ",
            ["y", "n"],
            "answer"
        )

        if answer == "y":
            tasks.remove(task)
            print("Task deleted!")
        else:
            print("Deletion cancelled.")



def run_menu(tasks):
    try:
        while True:
            print()
            for line in MENU:
                print(line)
            choice = ask_number("Choose: ", 0, 7)

            if choice == 1:
                add_task(tasks)
            elif choice == 2:
                show_tasks(order_tasks(tasks))
                input("\nPress Enter to the main menu...")
            elif choice == 3:
                show_task_details(tasks)
                input("\nPress Enter to the main menu...")
            elif choice == 4:
                mark_done(tasks)
                input("\nPress Enter to the main menu...")
            elif choice == 5:
                    print("TEST: OPTION 5 SELECTED")
                    import_files()
                    input("\nPress Enter to return to the main menu...")
            elif choice == 6:
                show_materials()
                input("\nPress Enter to the main menu...")
            elif choice == 7:
                  delete_task(tasks)
                  input("\nPress Enter to return to the main menu...")
       
            save_tasks(tasks)                 # save after every action
            if choice == 0:
                break
    except (EOFError, KeyboardInterrupt):     # Ctrl+C / Ctrl+D: leave without an error text
        print("\nSaving and exiting...")
        save_tasks(tasks)
    print("Successfully saved!")


def show_welcome():
    print("==============================")
    print("        STUDY COMPASS")
    print("==============================")
    print("Welcome to Study Compass!")
    print("Organize your tasks and study materials.")
    print()



def register():
    print()
    print("========== CREATE ACCOUNT ==========")

    username = input("Create username: ").strip()
    password = input("Create password: ").strip()

    if username == "" or password == "":
        print("Username and password cannot be empty.")
        return False

    with open("users.txt", "a") as file:
        file.write(username + "|" + password + "\n")

    print("Account created successfully!")
    return True


def login():
    print()
    print("================================")
    print("          USER LOGIN")
    print("================================")

    max_attempts = 4
    attempts = 0

    while attempts < max_attempts:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        with open("users.txt", "a+") as file:
            file.seek(0)
            for line in file:
                saved_username, saved_password = line.strip().split("|", 1)

                if username == saved_username and password == saved_password:
                    print()
                    print("================================")
                    print("       LOGIN SUCCESSFUL!")
                    print("================================")
                    return True

        attempts += 1
        remaining = max_attempts - attempts

        print()
        print("================================")
        print("         LOGIN FAILED")
        print("================================")
        print("Incorrect username or password.")

        if remaining > 0:
            print("Attempts remaining:", remaining)
            print("Please try again.")
        else:
            print("You have used all login attempts.")
            print("Returning to account menu.")

        print("================================")
        print()

    return False



def account_menu():
    while True:
        
        print("1.Sign up")
        print("2.Log in")
        print("0.Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            if login():
                return True
        elif choice == "0":
            return False
        else:
            print("Invalid choice.")




def main():
    make_folders()
    show_welcome()

    if account_menu():
        run_menu(load_tasks())
    else:
        print("Goodbye!")



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        print("Goodbye!")

