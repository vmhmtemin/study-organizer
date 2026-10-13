# StudyCompass (Study Organizer)

## Problem
Students often struggle to manage multiple academic tasks, keep track of deadlines, and decide which tasks to complete first. A close, difficult task can easily be forgotten behind an easier one, and a missed deadline is usually noticed too late. Organizing study materials can also be time-consuming: slides, PDFs, photos and recordings pile up in one folder with random names, so finding the right file for the right course takes time. This makes it difficult to maintain an efficient and organized study routine.

## Solution
StudyCompass is a task management and study material organization system.
- **Tasks:** students add tasks with a title, course, deadline and difficulty level (easy, medium, hard).
- **Priority:** every task gets a priority score, and the list is sorted so the most important task is always first.
- **Deadlines:** the application tracks deadlines and shows the number of days remaining for each task. Overdue tasks are clearly marked as `OVERDUE`, so important deadlines are not missed.
- **Study materials:** files dropped in `inbox/` are moved automatically into the right course folder (`materials/<course>/`), and a task can be linked to a file that can be opened from the menu.

Everything is managed in one place, which makes files easier to access and academic responsibilities easier to manage.

## How to run
Python 3 is needed. Open a terminal in the project folder, then:
```
python main.py                  # menu (asks for login first)
python cli.py <command> ...     # one command
python cli.py -h                # help
```
On a Mac, use `python3` instead of `python`.

**Example:**
```
python cli.py add --title Lab 2 --course python --deadline 2026-12-18 --difficulty hard --file lab2.pdf
python cli.py list              # tasks, most important first
python cli.py details --number 1
python cli.py done --number 1   # mark task 1 as done
python cli.py delete --number 1 # delete task 1 (asks y/n first)
python cli.py import            # move files from inbox/ to materials/<course>/
python cli.py materials         # show the stored files
python cli.py open --number 1   # show the path and size of task 1's file
python cli.py menu              # log in and open the full menu
```
Task numbers come from `list`. After `done` the task moves to the end, so run `list` again.
`inbox/`, `materials/` and `tasks.txt` are created automatically; `users.txt` is created at the first sign up.

**Flow:** `add` checks the input and saves the task → `list` calculates days left and the score of every task and sorts them → `import` sorts new files into course folders → the menu (option 3) finds the task's file and opens it with the computer's default program.

## First run and login
Run `python main.py`. On the first run choose **Sign up** to create an account, then **Log in**.
The task menu opens after a successful login. You have 4 attempts.
`python cli.py menu` uses the same login. The one-line CLI commands work on the local `tasks.txt` without a login.

Account rules:
- The username cannot be empty or contain `|`, and must not be taken already.
- The password must be at least 8 characters and contain both letters and numbers.

## Passwords
Passwords are never saved. `users.txt` only stores `username|hash`, for example `buse|895676405`.
- **Hash:** `simple_hash()` in `accounts.py` starts from 7 and, for every character, does `h = (h * 31 + ord(character)) % 1000000007`. Because of the multiplication, the order of the characters matters ("asd" and "dsa" give different numbers).
- **Salt:** the username (lower case) is put in front of the password before hashing, so two users with the same password get different hashes.
- **Login:** the typed password is hashed the same way and compared with the saved hash.
- **Limitation:** this is a simple hash made with class topics; short inputs can be reversed. Real systems use salted, slow hash functions.

## Logic
- `score = difficulty points (easy 1, medium 3, hard 5) + urgency * 2`
- Urgency from days left: 0-1 → 5, 2-3 → 4, 4-7 → 3, 8-14 → 2, more → 1. Passed deadline → `OVERDUE`.
- Same score → the task with the closer deadline comes first.
- Wrong input prints a warning instead of crashing.
- File names are checked against the course keywords in order; the first match decides the course. No match → `materials/unsorted/`.
- Unsupported types, unsafe names and symbolic links are skipped. Files are never overwritten.
- Opening a file: the menu opens it with the default program (`open_file`); `cli.py open` only shows its path and size (`show_file`).

## Files
| File | Job |
|---|---|
| `main.py` | menu, sign up and login |
| `cli.py` | argparse commands |
| `accounts.py` | password hashing and password checks |
| `tasks.py` | task dictionary, input checks, showing tasks |
| `priority.py` | days left, score, ordering |
| `materials.py` | import, list and open study files |
| `storage.py` | save / load `tasks.txt` |
| `contributions/` | what each group member did |

Created while running (not in Git): `inbox/` new files to import · `materials/` imported files by course · `tasks.txt` tasks · `users.txt` accounts.

## Not from the slides
`datetime.date` (today's date, `date.fromisoformat` for deadlines) · `os.startfile` / `os.system` / `os.name` (open a file on Windows or Mac) · `ord()` (character → number for the hash) · `str.isalpha()` / `str.isdigit()` (password check) · `rstrip()` (reading `users.txt`) · `EOFError` / `KeyboardInterrupt` (leaving the program with Ctrl+C / Ctrl+D).
