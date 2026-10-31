
# score = difficulty points + urgency * 2
from datetime import datetime, timedelta, UTC   # date/time values, durations and UTC
from zoneinfo import ZoneInfo                   # time zones, like "Europe/Istanbul"

DIFFICULTY = {"easy": 1, "medium": 3, "hard": 5} # store the points for each difficulty level
REMIND_DAYS = 3     # the reminder starts this many days before the deadline


def to_istanbul(moment):
    """The same moment in Istanbul time (a datetime with a UTC offset goes in)."""
    try:
        return moment.astimezone(ZoneInfo("Europe/Istanbul"))
    except KeyError:                       # this computer has no time zone data
        return moment + timedelta(hours=3) # Istanbul is UTC+3: datetime + timedelta


def get_today():
    """Today in Istanbul, as a datetime at midnight (strftime cuts off the clock time)."""
    now = to_istanbul(datetime.now(UTC))
    return datetime.fromisoformat(now.strftime("%Y-%m-%d"))


def days_left(deadline):
    """Days from today until the deadline ("2026-12-18"). Negative = already passed."""
    # fromisoformat() converts a date string (YYYY-MM-DD) into a datetime value
    return (datetime.fromisoformat(deadline) - get_today()).days  # deadline - today


def needs_reminder(task):
    """True when the task is not done and its deadline is at most REMIND_DAYS away."""
    if task["done"]:
        return False
    deadline = datetime.fromisoformat(task["deadline"])
    today = get_today()
    limit = today + timedelta(days=REMIND_DAYS)      # datetime + timedelta
    return deadline >= today and deadline <= limit   # a passed deadline (OVERDUE) gets no reminder


def get_score(task):
    """Score of a task, or "OVERDUE" if the deadline has passed."""
    days = days_left(task["deadline"])
    if days < 0:
        return "OVERDUE"
    elif days <= 1:
        urgency = 5
    elif days <= 3:
        urgency = 4
    elif days <= 7:
        urgency = 3
    elif days <= 14:
        urgency = 2
    else:
        urgency = 1
    return DIFFICULTY[task["difficulty"]] + urgency * 2   
# determine task priority using the difficulty and urgency scores


def is_better(task, other):

    if get_score(task) != get_score(other):
        return get_score(task) > get_score(other)
    return days_left(task["deadline"]) < days_left(other["deadline"])
# compare the priority scores of the two tasks


def order_tasks(tasks):

    waiting = []
    late = []
    finished = []
    for task in tasks:
        if task["done"]:
            finished.append(task)
        elif get_score(task) == "OVERDUE":
            late.append(task)
        else:
            waiting.append(task)
    # categorize each task based on its status and deadline

    # sorting the long way: take the best task out of `waiting`, again and again.
    ordered = []
    while len(waiting) > 0:
        best = waiting[0]
        for task in waiting:
            if is_better(task, best):    # find the highest-priority task in the waiting list
                best = task
        ordered.append(best)
        waiting.remove(best)
    return ordered + late + finished


if __name__ == "__main__":
    print(get_score({"deadline": "2100-01-01", "difficulty": "hard", "done": False}))   # 7
    print(get_score({"deadline": "2000-01-01", "difficulty": "hard", "done": False}))   # OVERDUE
