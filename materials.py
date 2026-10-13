# materials.py - move files from inbox/ to materials/<course>/ and open them
import os
import shutil

COURSES = {
    "python": "Advanced Python",
    "dsa": "Data Structures and Algorithms",
    "diffeq": "Differential Equations",
}

# words that can appear in a file name (lower case) -> course
KEYWORDS = {
    "python": ["python", "coe203"],
    "dsa": ["data structure", "data_structure", "data-structure", "swe209", "dsa", "algorithm"],
    "diffeq": ["differential", "math205", "diffeq", "diff eq", "diff_eq", "diff-eq"],
}

# accepted file types: extension -> label
FILE_TYPES = {
    "pdf": "Documents", "docx": "Documents", "txt": "Documents",
    "jpg": "Images", "jpeg": "Images", "png": "Images", "gif": "Images",
    "pptx": "Presentations", "ppt": "Presentations",
    "mp3": "Music",
}

# a file name with one of these characters is refused (it could break tasks.txt or the open command)
BAD_CHARACTERS = '|"$`\\;&<>*?\t\r\n'


def make_folders():
    os.makedirs("inbox", exist_ok=True)       # exist_ok=True: no error if it already exists
    for course in COURSES:
        os.makedirs(os.path.join("materials", course), exist_ok=True)
    os.makedirs(os.path.join("materials", "unsorted"), exist_ok=True)


def safe_name(filename):
    """False if the name contains one of the BAD_CHARACTERS."""
    for character in BAD_CHARACTERS:
        if character in filename:
            return False
    return True


def get_type(filename):
    """Label of the file type ("Documents" ...), or "" if the type is not accepted."""
    name = filename.lower()
    for extension in FILE_TYPES:
        if name.endswith("." + extension):    # endswith: does the name finish with ".pdf"?
            return FILE_TYPES[extension]
    return ""


def find_course(filename):
    """Looks for a keyword in the file name. No keyword gives "unsorted"."""
    name = filename.lower()
    for course in KEYWORDS:
        for word in KEYWORDS[course]:
            if word in name:
                return course
    return "unsorted"



def import_files():
    """Moves accepted files from inbox to the correct folder."""
    make_folders()

    print()
    print("========== IMPORT FILES ==========")

    filenames = sorted(os.listdir("inbox"))

    if len(filenames) == 0:
        print("Inbox is empty!")
        print("Put your files inside the inbox folder.")
        return

    moved = 0

    for filename in filenames:
        source = os.path.join("inbox", filename)

        if not os.path.isfile(source):
            print("Skipped (symobolic link):", filename)
            continue

        if not os.path.istifle(source):
            continue
    
        if not safe_name(filename):
            print("Skipped (unsafe file name):", filename)
            continue

        if get_type(filename) == "":
            print("Skipped (unsupported file type):", filename)
            continue

        course = find_course(filename)
        destination = os.path.join("materials", course, filename)

        if os.path.lexists(destination):
            print("Skipped (file already exists):", filename)
            continue

        
        try:
             shutil.move(source, destination)
             print("Imported:", filename)
             print("Course:", course)
             moved += 1
        except FileNotFoundError:
             print("Skipped (file no longer exists):", filename)
        except PermissionError:
             print("Skipped (permission denied):", filename)
        except OSError as error:
             print("Could not import", filename, ":", error)


    print("----------------------------------")
    print("Files imported:", moved)
    print("==================================")



def get_course_files(course):
    """Names of the accepted files stored for one course."""
    folder = os.path.join("materials", course)
    names = []
    if os.path.isdir(folder):
        for filename in sorted(os.listdir(folder)):
            if os.path.isfile(os.path.join(folder, filename)):
                if get_type(filename) != "" and safe_name(filename):
                    names.append(filename)
    return names


def show_course(course, title):
    print("\n" + title)
    for filename in get_course_files(course):
        print(f"  - {filename} [{get_type(filename)}]")


def show_materials():
    for course in COURSES:
        show_course(course, COURSES[course])
    show_course("unsorted", "Unsorted")


def show_file(course, filename):
    """Shows the file path and size."""
    if filename not in get_course_files(course):
        print("File not found:", filename)
        return

    path = os.path.join("materials", course, filename)

    try:
        size = os.path.getsize(path)
        print("File:", filename)
        print("Path:", path)
        print("Size:", size, "bytes")
    except FileNotFoundError:
        print("File no longer exists:", filename)
    except PermissionError:
        print("Permission denied:", filename)


if __name__ == "__main__":
    print(find_course("COE203_Advanced_Python_W2.pdf"))   # python
    print(find_course("DSA-week4.pptx"))                  # dsa
    print(find_course("holiday.mp3"))                     # unsorted
    print(get_type("Photo.JPG"), get_type("movie.mp4") == "")
