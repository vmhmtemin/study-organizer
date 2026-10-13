# StudyCompass (Study Organizer)

## Problem
Students often struggle to manage multiple academic tasks, keep track of deadlines, and decide which tasks to complete first. A close, difficult task can easily be forgotten behind an easier one, and a missed deadline is usually noticed too late. Organizing study materials can also be time-consuming: slides, PDFs, photos and recordings pile up in one folder with random names, so finding the right file for the right course takes time. This makes it difficult to maintain an efficient and organized study routine.

## Solution
StudyCompass is a task management and study material organization system.
- **Tasks:** students add tasks with a title, course, deadline and difficulty level (easy, medium, hard).
- **Priority:** every task gets a priority score, and the list is sorted so the most important task is always first.
- **Deadlines:** the application tracks deadlines and shows the number of days remaining for each task. Overdue tasks are clearly marked as `OVERDUE`, so important deadlines are not missed.
- **Study materials:** files dropped in `inbox/` are moved automatically into the right course folder (`materials/<course>/`), and a task can be linked to a file that opens with one command.

Everything is managed in one place, which makes files easier to access and academic responsibilities easier to manage.

## How to run
Python 3 is needed. Open a terminal in the project folder, then:
```
python main.py                  # menu
python cli.py <command> ...     # one command
python cli.py -h                # help
```

**Example:**
```
python cli.py add --title Lab 2 --course python --deadline 2026-12-18 --difficulty hard --file lab2.pdf
python cli.py list              # tasks, most important first
python cli.py details --number 1
python cli.py import            # move files from inbox/ to materials/<course>/
python cli.py materials         # show the stored files
python cli.py open --number 1   # open the file of task 1
python cli.py done --number 1   # mark task 1 as done
python cli.py open --number 1  # show the linked file's path and size
```
Task numbers come from `list`. After `done` the task moves to the end, so run `list` again.
`inbox/`, `materials/` and `tasks.txt` are created automatically.

**Flow:** `add` checks the input and saves the task → `list` calculates days left and the score of every task and sorts them → `import` sorts new files into course folders → `open` finds the task's file and opens it.

## First run and login

Run the application from the project folder:

    python main.py

On the first run, choose **Sign up** to create an account.
After registration, choose **Log in** and enter your credentials.
The task menu opens after a successful login.

The command-line interface is separate:

    python cli.py <command> ...

`python cli.py menu` opens the task menu directly and does not use
the login flow in `main.py`.


## Logic
- `score = difficulty points (easy 1, medium 3, hard 5) + urgency * 2`
- Urgency from days left: 0-1 → 5, 2-3 → 4, 4-7 → 3, 8-14 → 2, more → 1. Passed deadline → `OVERDUE`.
- Wrong input prints a warning instead of crashing.
- No keyword match in a file name → `materials/unsorted/`. Files are never overwritten.
- File names are checked against course keywords in order.
  The first matching keyword determines the course.
- If no keyword matches, the file goes to `materials/unsorted/`.
- `show_file` displays the file path and size; it does not open the file.


## Files
`main.py` menu · `cli.py` commands · `tasks.py` tasks and checks · `priority.py` score · `materials.py` files · `storage.py` `tasks.txt`


## Project folders and files

- `inbox/`: place new study files here before importing them.
- `materials/`: stores imported files in course folders.
- `contributions/`: project contributions or contribution guidelines,
  if included in the repository.
- `tasks.txt`: local task data; generated automatically.
- `users.txt`: local account data; should not be committed to Git.
- `__pycache__/`: Python-generated cache files; ignored by Git.

