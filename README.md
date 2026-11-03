# StudyCompass – Study Organizer
A command-line study management application designed to help students organize academic tasks, prioritize deadlines, and manage study materials efficiently.

## Project Overview
Students often need to manage multiple assignments, exams, deadlines, and course materials simultaneously. StudyCompass is a Python-based command-line application that brings these academic responsibilities together in one organized system. The application allows users to create accounts, manage academic tasks, calculate task priorities automatically, track deadlines, organize study materials by course, and monitor academic announcements through its Web Monitoring system.

## Problems
Students often struggle to manage multiple assignments, exams, and deadlines while keeping their course materials organized. Tracking different tasks manually can lead to missed deadlines, poor time management, and difficulty identifying which tasks require immediate attention. Additionally, study materials stored in different locations can make it harder to maintain an organized study routine and quickly access the required resources. Students may also miss important academic announcements and deadline changes when following multiple sources manually.

## Solutions
StudyCompass addresses these challenges by providing a centralized command-line study management system. It allows students to create and track academic tasks, automatically calculate priorities based on task difficulty and deadline urgency, and organize study materials into course-specific folders.

Its Web Monitoring feature processes academic announcements, detects deadline changes, and creates study tasks from relevant updates. By combining task management, deadline tracking, material organization, and announcement monitoring, StudyCompass helps students manage their academic responsibilities more efficiently.

## Key Features

### 1. Task Management
* Add tasks with a title, course, deadline, and difficulty level.
* View all tasks in an organized list.
* Display detailed information about individual tasks.
* Mark completed tasks as done.
* Delete tasks when they are no longer needed.

### 2. Priority Calculation
* Automatically calculate task priority scores.
* Consider both task difficulty and deadline urgency.
* Sort tasks from highest to lowest priority.
* Display overdue tasks with an `OVERDUE` label.

### 3. Deadline Tracking
* Calculate the remaining days until each deadline.
* Identify approaching deadlines.
* Automatically detect overdue tasks.

### 4. Study Material Organization
* Import files through the `inbox/` folder.
* Organize materials into course-specific folders.
* Support different file types, including documents, images, presentations, and audio files.
* View imported materials.
* Connect study files to tasks where supported.

### 5. User Authentication
* Create a user account through the sign-up system.
* Log in using a username and password.
* Validate account information.
* Limit login attempts.

### 6. Web Monitoring
* Process academic announcements from saved pages and JSON files.
* Validate announcement information, deadlines, and URLs.
* Navigate multiple linked pages with duplicate prevention.
* Detect deadline corrections and update existing tasks.
* Automatically create tasks from relevant academic announcements.

## Technologies Used
* Python 3
* Object-Oriented Programming concepts
* Argparse
* File Handling
* JSON Processing
* Date and Time Operations
* URL Parsing (`urllib.parse`)

## Project Structure

| **File / Folder** | **Description**                                                                                     |
| ----------------- | --------------------------------------------------------------------------------------------------- |
| `main.py`         | Main menu, sign-up, and login operations                                                            |
| `cli.py`          | Command-line interface and command management                                                       |
| `accounts.py`     | User authentication and password handling                                                           |
| `tasks.py`        | Task creation, validation, and display                                                              |
| `priority.py`     | Priority score calculation and task sorting                                                         |
| `materials.py`    | Study material importing and organization                                                           |
| `storage.py`      | Task data storage and retrieval                                                                     |
| `web.py`          | Web monitoring, announcement validation, deadline correction detection, and automatic task creation |
| `contributions/`  | Individual group member contributions                                                               |

The following folders and files are used by the application:

* `inbox/` – Files waiting to be imported.
* `materials/` – Imported study materials organized by course.
* `tasks.txt` – Stored task information.
* `users.txt` – User account information.

## How to Use

### Starting the Application
```bash
python main.py
```
On the first run, create an account using the Sign Up option. Then log in to access the main menu.

### Command-Line Operations
You can also use individual commands through `cli.py`.

| **Command** | **Description**                                       |
| ----------- | ----------------------------------------------------- |
| `add`       | Add a new task                                        |
| `list`      | Display tasks sorted by priority                      |
| `details`   | View task details                                     |
| `done`      | Mark a task as completed                              |
| `delete`    | Delete a task                                         |
| `open`      | Access associated file information                    |
| `import`    | Import study materials                                |
| `materials` | Display imported materials                            |
| `monitor`   | Monitor academic announcements and update study tasks |
| `menu`      | Open the application menu                             |

### Example Commands
Add a task:
```bash
python cli.py add --title Lab 2 --course python --deadline 2026-12-18 --difficulty hard
```

Display tasks:
```bash
python cli.py list
```

View task details:
```bash
python cli.py details --number 1
```

Mark a task as completed:
```bash
python cli.py done --number 1
```

Delete a task:
```bash
python cli.py delete --number 1
```

## Task Priority System
StudyCompass calculates task priorities using difficulty and deadline urgency.

**Difficulty Points:**
| **Difficulty** | **Points** |
| -------------- | ---------- |
| Easy           | 1          |
| Medium         | 3          |
| Hard           | 5          |

**Deadline Urgency:**
| **Days Remaining** | **Urgency** |
| ------------------ | ----------- |
| 0–1 days           | 5           |
| 2–3 days           | 4           |
| 4–7 days           | 3           |
| 8–14 days          | 2           |
| More than 14 days  | 1           |

**Priority Formula:**
`Priority Score = Difficulty Points + (Urgency × 2)`
Tasks with higher scores appear first. Overdue tasks are identified separately.

## Study Material Management
Study materials can be imported by placing files inside the `inbox/` folder.
Run:
```bash
python cli.py import
```
Imported files are organized into course folders:
```text
materials/
    python/
    dsa/
    diffeq/
    unsorted/
```
To display imported materials:
```bash
python cli.py materials
```

## Web Monitoring
The Web Monitoring module (`web.py`) helps students track academic announcements and important deadline updates.
* Processes announcements from built-in sample pages or local JSON files.
* Validates announcement information and allowed URLs.
* Follows linked pages with a maximum limit of five pages.
* Detects deadline corrections and updates existing tasks.
* Creates new study tasks from relevant academic announcements.

### Running Web Monitoring
To run the monitoring system:
```bash
python cli.py monitor
```
To process a custom JSON file:
```bash
python cli.py monitor --source announcements.json
```
**Note:** The current implementation processes saved page data and local JSON files rather than continuously fetching information from live websites.

## User Authentication
Users can create accounts and log in through the application menu.
Account features include:
* Username validation.
* Unique username checking.
* Password validation.
* Limited login attempts.
* Password hashing.
The application stores password hashes rather than plain-text passwords.
