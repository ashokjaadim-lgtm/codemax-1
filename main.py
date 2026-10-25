import csv
import json
from pathlib import Path

DATA_DIR = Path("data")
JSON_FILE = DATA_DIR / "students.json"
CSV_FILE = DATA_DIR / "students.csv"


def ensure_data_files():
    """Create the data folder and an empty JSON file if needed."""
    DATA_DIR.mkdir(exist_ok=True)
    if not JSON_FILE.exists():
        save_students([])


def load_students():
    """Load student records from JSON. Return an empty list if file is empty/missing."""
    ensure_data_files()
    try:
        with JSON_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        print("Warning: students.json is invalid. Starting with an empty list.")
        return []
    except OSError as error:
        print(f"Could not read student data: {error}")
        return []


def save_students(students):
    """Save student records to JSON."""
    DATA_DIR.mkdir(exist_ok=True)
    try:
        with JSON_FILE.open("w", encoding="utf-8") as file:
            json.dump(students, file, indent=4, ensure_ascii=False)
    except OSError as error:
        print(f"Could not save student data: {error}")


def get_next_id(students):
    """Return the next available numeric student ID."""
    return max((student["id"] for student in students), default=0) + 1


def add_student(students):
    """Create a student record."""
    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    try:
        age = int(input("Enter age: "))
        marks = float(input("Enter marks (0-100): "))
        if age <= 0:
            raise ValueError("Age must be greater than zero.")
        if not 0 <= marks <= 100:
            raise ValueError("Marks must be between 0 and 100.")
    except ValueError as error:
        print(f"Invalid input: {error}")
        return

    student = {
        "id": get_next_id(students),
        "name": name,
        "age": age,
        "marks": marks
    }
    students.append(student)
    save_students(students)
    print(f"Student added successfully. ID: {student['id']}")


def display_students(students):
    """Read and display all records."""
    if not students:
        print("No student records found.")
        return

    print("\n{:<6} {:<25} {:<8} {:<10} {:<10}".format(
        "ID", "NAME", "AGE", "MARKS", "RESULT"
    ))
    print("-" * 62)
    # List comprehension example: build a list of formatted rows.
    rows = [
        (s["id"], s["name"], s["age"], s["marks"],
         "Pass" if s["marks"] >= 40 else "Needs improvement")
        for s in students
    ]
    for row in rows:
        print("{:<6} {:<25} {:<8} {:<10.2f} {:<10}".format(*row))


def find_student(students, student_id):
    """Find one student by ID using a lambda function."""
    return next(filter(lambda student: student["id"] == student_id, students), None)


def search_student(students):
    try:
        student_id = int(input("Enter student ID to search: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    student = find_student(students, student_id)
    if student:
        print(f"Found: ID={student['id']}, Name={student['name']}, "
              f"Age={student['age']}, Marks={student['marks']}")
    else:
        print("Student not found.")


def update_student(students):
    try:
        student_id = int(input("Enter student ID to update: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    student = find_student(students, student_id)
    if not student:
        print("Student not found.")
        return

    print("Press Enter to keep the current value.")
    name = input(f"Name [{student['name']}]: ").strip()
    age_text = input(f"Age [{student['age']}]: ").strip()
    marks_text = input(f"Marks [{student['marks']}]: ").strip()

    try:
        if name:
            student["name"] = name
        if age_text:
            age = int(age_text)
            if age <= 0:
                raise ValueError("Age must be greater than zero.")
            student["age"] = age
        if marks_text:
            marks = float(marks_text)
            if not 0 <= marks <= 100:
                raise ValueError("Marks must be between 0 and 100.")
            student["marks"] = marks
    except ValueError as error:
        print(f"Invalid input: {error}. No changes saved.")
        return

    save_students(students)
    print("Student updated successfully.")


def delete_student(students):
    try:
        student_id = int(input("Enter student ID to delete: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    student = find_student(students, student_id)
    if not student:
        print("Student not found.")
        return

    confirm = input(f"Delete {student['name']}? (y/n): ").strip().lower()
    if confirm == "y":
        students.remove(student)
        save_students(students)
        print("Student deleted successfully.")
    else:
        print("Delete cancelled.")


def export_to_csv(students):
    """Export JSON-backed records to CSV."""
    DATA_DIR.mkdir(exist_ok=True)
    fieldnames = ["id", "name", "age", "marks"]
    try:
        with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students)
        print(f"Exported {len(students)} record(s) to {CSV_FILE}.")
    except OSError as error:
        print(f"Could not export CSV: {error}")


def show_topper(students):
    if not students:
        print("No records available.")
        return
    # Lambda example: sort records by marks, highest first.
    ranked = sorted(students, key=lambda student: student["marks"], reverse=True)
    topper = ranked[0]
    print(f"Topper: {topper['name']} with {topper['marks']:.2f} marks.")


def show_menu():
    print("""
========== STUDENT RECORD MANAGEMENT ==========
1. Add student
2. View all students
3. Search student by ID
4. Update student
5. Delete student
6. Export records to CSV
7. Show topper
0. Exit
===============================================
""")


def main():
    students = load_students()
    while True:
        try:
            show_menu()
            choice = input("Choose an option: ").strip()
            if choice == "1":
                add_student(students)
            elif choice == "2":
                display_students(students)
            elif choice == "3":
                search_student(students)
            elif choice == "4":
                update_student(students)
            elif choice == "5":
                delete_student(students)
            elif choice == "6":
                export_to_csv(students)
            elif choice == "7":
                show_topper(students)
            elif choice == "0":
                print("Thank you for using Student Record Management System!")
                break
            else:
                print("Invalid choice. Please select 0-7.")
        except (KeyboardInterrupt, EOFError):
            print("\nProgram stopped safely.")
            break
        except Exception as error:
            # Catch unexpected errors without crashing the menu.
            print(f"Unexpected error: {error}")
        finally:
            # Runs after each menu action, even if an error occurs.
            pass


if __name__ == "__main__":
    main()
