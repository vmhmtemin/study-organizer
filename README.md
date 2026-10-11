# Study Organizer

A small command-line program that ranks homework by priority and keeps study files
(pdf, jpg, pptx, mp3 ...) sorted by course. Courses: `python`, `dsa`, `diffeq`.

## Run
```
python main.py                  # menu
python cli.py <command> ...     # one command, e.g. python cli.py list
python cli.py -h                # help
```

## Commands (cli.py)
| Command | What it does |
|---|---|
| `add --title Lab 2 --course python --deadline 2026-12-18 --difficulty hard [--file name.pdf]` | add a task |
| `list` | show tasks, most important first |
| `details --number N` / `done --number N` / `open --number N` | show, finish, or open the file of task N (N = number from `list`) |
| `import` | move files from `inbox/` to `materials/<course>/` |
| `materials` | show the stored files |
| `menu` | open the menu |

Deadline format: `YYYY-MM-DD` (year-month-day). Difficulty: `easy`, `medium`, `hard`.
Wrong input never crashes the program: it prints a warning (the menu asks again).

## Files
| File | Job |
|---|---|
| `main.py` | the menu |
| `cli.py` | argparse commands |
| `tasks.py` | task dictionary, input checks, showing tasks |
| `priority.py` | days left, score, ordering |
| `materials.py` | import, sort and open files |
| `storage.py` | save / load `tasks.txt` |

`inbox/`, `materials/` and `tasks.txt` are created automatically.

## Priority score
`score = difficulty points + urgency * 2` (easy 1, medium 3, hard 5).
Days left = deadline - today. 0-1 days → urgency 5, 2-3 → 4, 4-7 → 3, 8-14 → 2, more → 1.
Deadline passed → `OVERDUE` (no score). Same score → the closer deadline comes first.

## Sorting files
The course is found from words in the file name (`KEYWORDS` in `materials.py`), for example
`coe203` → python, `dsa` or `swe209` → dsa, `math205` or `diffeq` → diffeq.
No match → `materials/unsorted/`. Other file types are skipped, and files are never overwritten.

Not from the slides: `datetime.date` (today's date), `os.startfile` / `os.system` (open a file).
