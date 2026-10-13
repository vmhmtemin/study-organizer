# Member 5
Name: Mehmet Emin Soyal
Student ID: 2509111011
GitHub username: vmhmtemin

## My files
- `accounts.py` (new file): password hashing and password checks
- `main.py`: connected the hashing to `register()` and `login()`
- `materials.py`: bug fixes and comments
- `cli.py`: bug fixes, login for `python cli.py menu`
- `README.md`, `.gitignore`

## My functions
- `accounts.py`: `simple_hash`, `hash_password`, `check_password`
- `main.py`: hashing inside `register()` and `login()`
- `materials.py`: `open_file` (restored), the checks inside `import_files`

## What I did
- Created the GitHub repository and invited the group members.
- **Password hashing:** at first the login compared plain-text passwords from `users.txt`, so anyone who opened the file could read every password. I wrote `simple_hash()`, which turns a text into a number: it starts from 7 and, for every character, multiplies by 31 and adds `ord(character)`, then takes `% 1000000007` so the number stays in a fixed range.
- **Salt:** `hash_password()` puts the username in front of the password before hashing. Two users with the same password now get different hashes.
- **Password rules:** `check_password()` refuses passwords shorter than 8 characters or without both letters and numbers.
- **Login:** `register()` now saves `username|hash` instead of the password, and `login()` hashes the typed password and compares the two hashes.
- **Git:** fixed `.gitignore` so `users.txt` and `.DS_Store` are not uploaded, and removed them from the repository.
- **Bug fixes:** restored `open_file` (the menu could not start), fixed a duplicate `--number` argument (every CLI command crashed), and fixed a typo in `import_files` (importing any file crashed).
- `python cli.py menu` now asks for a login, like `main.py`.
- Added comments to `materials.py` and updated the README (login, passwords, files, things not from the slides).

## Class topics I used
- **Strings and loops:** `for character in text` to go through every character of the password
- **Arithmetic operators:** `*`, `+` and `%` in the hash formula
- **Type conversion:** `str(hash_password(...))`, because `users.txt` is read as text and the hash is a number
- **Functions and return values:** every check returns a warning text, or `""` when the input is fine
- **Conditionals and booleans:** `has_letter` / `has_digit` flags with `not` and `or`
- **String methods:** `lower()`, `strip()`
- **Modules and imports:** `from accounts import check_password, hash_password`
- **`if __name__ == "__main__":`** for quick tests
- **Not from the slides:** `ord()` (character → number), `isalpha()` / `isdigit()` (letter / digit check)

## Problems I had and how I fixed them
- **The hash could be reversed:** with short passwords the modulo does nothing, so the number can be split back into characters ("asd" → 305419 → 97, 115, 100). I added the username as a salt and a minimum password length. I wrote the remaining limitation in the README.
- **`users.txt` was still uploaded:** `.gitignore` had `users.txt/`; the `/` at the end means "folder", so the file was not ignored. I removed the `/` and ran `git rm --cached users.txt`.
- **Login always failed after hashing:** `load_users()` reads the hash as text (`"895676405"`) but `hash_password()` returns a number. I converted the number with `str()` before comparing.
- **`ImportError: cannot import name 'open_file'`:** a new version of `materials.py` had replaced `open_file` with `show_file`, but `main.py` still used `open_file`. I added `open_file` back and kept `show_file` for the CLI.
- **`argparse.ArgumentError: conflicting option string: --number`:** `--number` was added twice in `cli.py`. I kept only one.
- **`AttributeError: ... no attribute 'istifle'`:** a typo in `import_files`. I replaced it with `os.path.islink` (skip symbolic links) and `os.path.isfile` (skip folders).

## How I tested my part
- `python accounts.py`: checked the example hashes ("asd" → 305419) against a hand calculation.
- Sign up with `123` → "Password must be at least 8 characters".
- Sign up with a valid password → `users.txt` contains `username|number`, not the password.
- Same username again → "This username already exists".
- Correct password → login successful; wrong password → "Attempts remaining: 3".
- Empty line in `users.txt` → login still works, no crash.
- `python cli.py menu` → asks for a login.
- Put a `.pdf`, an `.exe` and a file with `;` in its name into `inbox/` and ran `python cli.py import` → only the `.pdf` is imported, the other two are skipped.
