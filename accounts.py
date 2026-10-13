# accounts.py - password hashing and password checks (used by register() and login() in main.py)
# users.txt keeps one user per line:  buse|895676405
# The password itself is never saved, only its hash.

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


# ---- check: returns a warning text, or "" when everything is fine ----

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


# quick test: runs only with "python accounts.py"
if __name__ == "__main__":
    print(simple_hash("asd"))                      # 305419
    print(hash_password("ali", "asd"))             # 92518556
    print(hash_password("ayse", "asd"))            # 249591819 (same password, other hash)
    print(check_password("123"))                   # too short
    print(check_password("gizli1234") == "")       # True
