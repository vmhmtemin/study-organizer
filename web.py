# web.py - web monitoring: read saved announcements, check them, and turn them into useful actions
import json
from datetime import datetime
from urllib.parse import urljoin

from materials import COURSES, find_course
from priority import days_left, to_istanbul
from storage import load_deadlines, save_deadlines, save_tasks
from tasks import check_task, new_task

SOURCE = "page1"                              # the saved sample below: no website is contacted
BASE_URL = "https://campus.example/news/"     # relative links are joined to this page
ALLOWED_HOST = "https://campus.example/"      # only links that start with this are accepted
MAX_PAGES = 5                                 # request limit for the chain of pages

# A saved sample response (two pages). Page 1 points to page 2 with "next".
SAMPLE_PAGES = {
    "page1": {
        "items": [
            {"id": "A1", "title": "  Python   Study Night  ", "url": "/events/A1", "deadline": "2027-03-21T22:00:00+00:00"},
            {"id": "A2", "title": "DSA Workshop", "url": "/events/A2", "deadline": "2027-03-25T15:00:00+00:00"},
        ],
        "next": "page2",
    },
    "page2": {
        "items": [
            {"id": "A2", "title": "DSA Workshop", "url": "/events/A2", "deadline": "2027-03-25T15:00:00+00:00"},
            {"id": "A3", "title": "Mathematics Seminar", "url": "/events/A3", "deadline": "2027-03-28T15:00:00+00:00"},
            {"id": "A4", "title": "Python Pizza Night", "url": "https://other.example/x", "deadline": "2027-03-26T15:00:00+00:00"},
            {"id": "A5", "title": "Algorithm Review", "url": "/events/A5", "deadline": "03/04/2026"},
            {"id": "  ", "title": "Python Empty Id", "url": "/events/A6", "deadline": "2027-03-26T15:00:00+00:00"},
        ],
    },
}


# ---- shared helpers: UTC text -> Istanbul time ----

def show_time(deadline):
    """'2026-11-21T22:00:00+00:00' -> '22 Nov, 01:00' (Istanbul time)."""
    try:
        local = to_istanbul(datetime.fromisoformat(deadline))
    except ValueError:
        return "unknown time"
    return local.strftime("%d %b, %H:%M")


def istanbul_date(deadline):
    try:
        local = to_istanbul(datetime.fromisoformat(deadline))
    except ValueError:
        return ""                             # the text cannot be read
    return local.strftime("%Y-%m-%d")         # the day we store in tasks.txt


# ---- reading infrastructure (the minimum that features 4 and 5 need) ----

def read_page(filename):
    """One saved page -> (list of raw records, name of the next page or "", problem)."""
    try:
        if filename in SAMPLE_PAGES:
            data = SAMPLE_PAGES[filename]         # the built-in sample
        else:
            raw = ""
            with open(filename, encoding="utf-8") as file:
                for line in file:
                    raw += line
            data = json.loads(raw)                # JSON text becomes Python values
        items = data["items"]                     # one container at a time
    except FileNotFoundError:
        return [], "", f"source '{filename}' was not found"
    except ValueError:                            # the text is not JSON
        return [], "", f"'{filename}' is not valid JSON"
    except (KeyError, TypeError):                 # wrong fields: nothing to trust
        return [], "", f"'{filename}' has no 'items' list"
    next_page = ""
    if "next" in data:
        next_page = data["next"]
    return items, next_page, ""


# ---- FEATURE 4: clean and check one record ----

def clean_record(raw):
    """Returns (record, "") or (None, problem). A bad record is never repaired by guessing."""
    for field in ["id", "title", "url", "deadline"]:
        if field not in raw:
            return None, f"missing field '{field}'"
    record_id = str(raw["id"]).strip()
    if record_id == "" or "|" in record_id:
        return None, "id is empty or contains |"
    title = " ".join(str(raw["title"]).split())       # strip + split + join: one space between words
    if title == "":
        return None, "title is empty"
    url = urljoin(BASE_URL, str(raw["url"]).strip())  # relative link + base URL
    if url[:len(ALLOWED_HOST)] != ALLOWED_HOST:
        return None, "link is not on the allowed host"
    deadline = str(raw["deadline"]).strip()
    if deadline[-6:] != "+00:00":
        return None, "deadline needs an explicit +00:00 offset"
    try:
        datetime.fromisoformat(deadline)
    except ValueError:
        return None, f"deadline '{deadline[:25]}' cannot be read"
    return {"id": record_id, "title": title, "url": url, "deadline": deadline}, ""


# ---- FEATURE 5: read every page, keep one record per ID ----

def read_pages(first_page):
    """Returns (raw records by id, records without an id, pages read, problem)."""
    by_id = {}                    # each key is an ID, its value is the whole record
    no_id = []
    visited = []                  # remember page links: a repeated link would be a loop
    page = first_page
    while page != "":
        if page in visited:
            print("Stopped: the next page link repeats:", page)
            break
        if len(visited) >= MAX_PAGES:
            print("Stopped: request limit reached.")
            break
        visited.append(page)
        items, next_page, problem = read_page(page)
        if problem != "":
            return {}, [], len(visited), problem   # one failed page = the whole scan failed
        try:
            for raw in items:
                try:
                    by_id[str(raw["id"]).strip()] = raw   # same ID again replaces the old copy
                except (KeyError, TypeError):
                    no_id.append(raw)
        except TypeError:
            return {}, [], len(visited), f"'{page}': 'items' is not a list"
        page = next_page
    return by_id, no_id, len(visited), ""


# ---- FEATURE 7: deadline corrections ----

def find_corrections(records, old):
    """records = {id: record}, old = {id: deadline text}. Returns [(record, old deadline)]."""
    corrections = []
    for record_id in records:
        if record_id in old and old[record_id] != records[record_id]["deadline"]:
            corrections.append((records[record_id], old[record_id]))
    return corrections


def show_correction(record, old_deadline):
    print("DEADLINE CORRECTED!")
    print("  " + record["title"])
    print("  Previous:", show_time(old_deadline))
    print("  New:", show_time(record["deadline"]), "Istanbul")


def move_task_deadline(tasks, record):
    """Moves the deadline of the task we already have. True if a task changed."""
    deadline = istanbul_date(record["deadline"])
    if deadline == "":
        return False
    for task in tasks:
        if task["title"] == record["title"] and task["deadline"] != deadline:
            task["deadline"] = deadline
            return True
    return False


# ---- FEATURE 9: useful alert + task ----

def announce(record, tasks):
    """Alerts about a new relevant announcement and adds it as a task. True if tasks changed."""
    course = find_course(record["title"])              # the same keyword rule as the study files
    if course == "unsorted":
        return False                                   # not one of our courses: not relevant
    deadline = istanbul_date(record["deadline"])
    if deadline == "":
        print("Task not added: the deadline cannot be read.")
        return False
    if days_left(deadline) < 0:
        return False                                   # the deadline has already passed
    for task in tasks:
        if task["title"] == record["title"] and task["course"] == course:
            return False                               # we already have this task: not new
    problem = check_task(record["title"], course, deadline, "medium")
    if problem != "":
        print("Task not added:", problem)
        return False
    print("NEW ANNOUNCEMENT!")
    print("  " + record["title"])
    print("  Course:", COURSES[course])
    print("  Deadline:", show_time(record["deadline"]), "Istanbul")
    print("  Review the source and apply:", record["url"])
    tasks.append(new_task(record["title"], course, deadline, "medium", ""))
    print("Task added:", record["title"])
    return True


# ---- one scan: the features work one after another, each one on its own data ----

def run_monitor(source, tasks):
    raws, no_id, pages, problem = read_pages(source)                    # feature 5
    if problem != "":
        print("Scan failed:", problem)
        print("Nothing was changed.")
        return

    records = {}
    rejected = []
    for record_id in raws:                                              # feature 4
        record, why = clean_record(raws[record_id])
        if record is None:
            rejected.append(why + "  <- " + str(raws[record_id])[:50])
        else:
            records[record["id"]] = record
    for raw in no_id:
        rejected.append("missing field 'id'  <- " + str(raw)[:50])

    old = load_deadlines()
    changed = False
    for record, old_deadline in find_corrections(records, old):         # feature 7
        show_correction(record, old_deadline)
        if move_task_deadline(tasks, record):
            print("Task deadline updated:", record["title"])
            changed = True
    for record_id in records:                                           # feature 9
        if announce(records[record_id], tasks):
            changed = True

    for record_id in records:
        old[record_id] = records[record_id]["deadline"]                 # remember the newest deadline
    save_deadlines(old)
    if changed:
        save_tasks(tasks)
    for line in rejected:
        print("  Rejected:", line)
    print(f"Scan finished: {len(records)} valid, {len(rejected)} rejected. Pages: {pages}.")
