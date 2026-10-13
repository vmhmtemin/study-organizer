# accounts.py - user accounts with hashed passwords (users.txt)
#   one user per line:  mehmet|92518556
# The password itself is never saved, only its hash.

USERS_FILE = "users.txt"
MIN_PASSWORD_LENGTH = 8


# ---- hashing ----

def simple_hash(text):
    """Turns a text into a number. The same text always gives the same number."""
    h = 7
    for character in text:
        h = (h * 31 + ord(character)) % 1000000007   # ord("a") = 97
    return h


def hash_password(username, password):
    """The username is the salt: two users with the same password get different hashes."""
    return simple_hash(username.lower() + password)


# ---- checks: each returns a warning text, or "" when everything is fine ----

def check_username(username):
    if username == "":
        return "Username cannot be empty."
    if len(username) > 20:
        return "Username is too long (maximum 20 characters)."
    if "|" in username or " " in username:
        return "Username cannot contain | or spaces."
    return ""


def check_password(password):
    if len(password) < MIN_PASSWORD_LENGTH:
        return f"Password must be at least {MIN_PASSWORD_LENGTH} characters."
    has_letter = False
    has_digit = False
    for character in password:
        if character.isalpha():
            has_letter = True
        if character.isdigit():
            has_digit = True
    if not has_letter or not has_digit:
        return "Password must contain letters and numbers."
    return ""


# ---- users.txt ----

def load_users():
    """Returns a dictionary {username: hash}."""
    users = {}
    try:
        with open(USERS_FILE, encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 2 and parts[1].isdigit():   # a damaged line is skipped
                    users[parts[0]] = int(parts[1])
    except FileNotFoundError:
        pass                                  # first run: there is no file yet
    return users


def register(username, password):
    """Creates a new user. Returns a warning text, or "" if it worked."""
    username = username.strip().lower()
    problem = check_username(username)
    if problem == "":
        problem = check_password(password)
    if problem != "":
        return problem
    if username in load_users():
        return "This username is already taken."
    with open(USERS_FILE, "a", encoding="utf-8") as file:     # "a" adds to the end
        file.write(f"{username}|{hash_password(username, password)}\n")
    return ""


def check_login(username, password):
    """Hashes the entered password the same way and compares it with the saved hash."""
    username = username.strip().lower()
    users = load_users()
    if username not in users:
        return False
    return hash_password(username, password) == users[username]


if __name__ == "__main__":
    print(simple_hash("asd"))                      # 305419
    print(hash_password("ali", "asd"))             # 92518556
    print(hash_password("ayse", "asd"))            # 249591819 (same password, other hash)
    print(check_password("123"))                   # too short
