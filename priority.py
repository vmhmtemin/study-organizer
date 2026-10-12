
# score = difficulty points + urgency * 2
from datetime import date     # date.today() gives today's date

DIFFICULTY = {"easy": 1, "medium": 3, "hard": 5} # store the points for each difficulty level


def days_left(deadline):
    """Days from today until the deadline ("2026-12-18"). Negative = already passed."""
    # fromisoformat() converts a date string (YYYY-MM-DD) into a date object
    return (date.fromisoformat(deadline) - date.today()).days  # deadline - date of today


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
