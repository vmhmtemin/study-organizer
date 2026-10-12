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
## Uploading Files
1. Copy your study materials into the `inbox` folder.
2. Run `py cli.py import` to import the files.
3. Run `py cli.py materials` to view your uploaded materials.


**Example:**
```
python cli.py add --title Lab 2 --course python --deadline 2026-12-18 --difficulty hard --file lab2.pdf
python cli.py list              # tasks, most important first
python cli.py details --number 1
python cli.py import            # move files from inbox/ to materials/<course>/
python cli.py materials         # show the stored files
python cli.py open --number 1   # open the file of task 1
python cli.py done --number 1   # mark task 1 as done
```
Task numbers come from `list`. After `done` the task moves to the end, so run `list` again.
`inbox/`, `materials/` and `tasks.txt` are created automatically.

**Flow:** `add` checks the input and saves the task → `list` calculates days left and the score of every task and sorts them → `import` sorts new files into course folders → `open` finds the task's file and opens it.

## Logic
- `score = difficulty points (easy 1, medium 3, hard 5) + urgency * 2`
- Urgency from days left: 0-1 → 5, 2-3 → 4, 4-7 → 3, 8-14 → 2, more → 1. Passed deadline → `OVERDUE`.
- Wrong input prints a warning instead of crashing.
- No keyword match in a file name → `materials/unsorted/`. Files are never overwritten.

## Files
`main.py` menu · `cli.py` commands · `tasks.py` tasks and checks · `priority.py` score · `materials.py` files · `storage.py` `tasks.txt`
