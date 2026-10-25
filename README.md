# Student Record Management System

A beginner-friendly Python CLI project for the **Functions, Files & Exception Handling (Day 6–Day 10)** module.

## Features
- Add, view, search, update and delete student records (CRUD)
- Save data persistently in `data/students.json`
- Export records to `data/students.csv`
- Find the topper
- Input validation and exception handling
- Uses functions, parameters, return values, a lambda function and list comprehension

## Requirements
- Python 3.10 or newer
- No external Python packages required

## Run in VS Code (Windows)
1. Download or clone this repository.
2. Open the project folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment:
   ```powershell
   python -m venv .venv
   ```
5. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt terminal and run:
   ```bat
   .venv\Scripts\activate.bat
   ```
6. Run the program:
   ```powershell
   python main.py
   ```

## Menu
1. Add student
2. View all students
3. Search student by ID
4. Update student
5. Delete student
6. Export records to CSV
7. Show topper
0. Exit

## Data files
The program creates the `data` folder and `students.json` automatically. Choose **Export records to CSV** to create/update `students.csv`.

## Concepts demonstrated
- **Functions:** `add_student()`, `load_students()`, `save_students()`, etc.
- **Parameters and return values:** functions receive student lists and return results.
- **Lambda:** student lookup and sorting by marks.
- **List comprehension:** creating formatted display rows.
- **File handling:** `with open(...)` and `pathlib.Path`.
- **JSON and CSV:** JSON is the main storage format; CSV is available for export.
- **Exception handling:** `try`, `except`, and `finally`.
- **Virtual environment:** `.venv` keeps the project environment separate.

## Example test
Add:
- Name: Asha
- Age: 19
- Marks: 86.5

Then view all students, search using the shown ID, update the marks, export to CSV, and try deleting the record.

## Notes
- Student records are stored locally on your computer.
- Do not commit real personal student information to a public repository.
