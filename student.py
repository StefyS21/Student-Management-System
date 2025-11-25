import csv
import os

# --- Configuration ---
FILE_NAME = 'students.txt'
FIELDNAMES = ['ID', 'Name', 'Age', 'Grade', 'GPA']

class Student:
    """Represents a student with basic details."""
    def __init__(self, student_id, name, age, grade, gpa):
        # Initializing object attributes
        self.id = student_id
        self.name = name
        # Using try-except for robust initialization against file corruption
        try:
            self.age = int(age)
        except ValueError:
            self.age = 0
            
        self.grade = grade
        try:
            self.gpa = float(gpa)
        except ValueError:
            self.gpa = 0.0

    def __str__(self):
        """Returns a formatted string for display."""
        return (f"ID: {self.id:<5} | Name: {self.name:<20} | Age: {self.age:<3} | "
                f"Grade: {self.grade:<5} | GPA: {self.gpa:.2f}")

    def to_dict(self):
        """Converts the Student object to a dictionary for CSV writing."""
        return {
            'ID': self.id,
            'Name': self.name,
            'Age': self.age,
            'Grade': self.grade,
            'GPA': self.gpa
        }

# --- File Handling (Load/Save) ---

def load_students():
    """Loads student records from the CSV file."""
    students = []
    # Create file with headers if it doesn't exist (File Handling)
    if not os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writeheader()
            return students
        except Exception as e:
            print(f"Error creating file: {e}")
            return students

    # Load existing data
    try:
        with open(FILE_NAME, 'r', newline='') as f:
            reader = csv.DictReader(f, fieldnames=FIELDNAMES)
            next(reader) # Skip the header row
            for row in reader: # Looping through file data
                try:
                    # Creating Student objects from file data
                    if all(key in row for key in FIELDNAMES):
                        student = Student(row['ID'], row['Name'], row['Age'], row['Grade'], row['GPA'])
                        students.append(student)
                except Exception as e:
                    # Exception Handling for corrupted data rows
                    print(f"Skipping corrupted record: {row} -> Error: {e}")
        return students
    except Exception as e:
        print(f"An error occurred during file loading: {e}")
        return students


def save_students(students):
    """Saves the list of Student objects back to the CSV file."""
    try:
        with open(FILE_NAME, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            for student in students:
                writer.writerow(student.to_dict()) # Writing dictionary to file
        print(f"\n--- Data saved successfully to {FILE_NAME} ---")
    except Exception as e:
        print(f"\n!!! ERROR: Could not save data to file. {e} !!!")

# --- Core Features (Functions) ---

def get_next_id(students):
    """Generates the next sequential ID."""
    if not students:
        return 1001
    
    max_id = 0
    for student in students:
        try:
            max_id = max(max_id, int(student.id))
        except ValueError:
            continue
    return max_id + 1

def add_new_student(students):
    """Implements 'New Student - add' feature with data validation."""
    print("\n--- New Student Addition ---")
    student_id = str(get_next_id(students))
    
    name = input("Enter Name: ").strip()
    if not name:
        print("Name cannot be empty. Operation cancelled.")
        return

    while True: # Loop for age input validation
        try:
            age = int(input("Enter Age: "))
            if age <= 0:
                print("Age must be a positive number.")
                continue
            break
        except ValueError: # Exception Handling
            print("Invalid input. Please enter a number for Age.")

    grade = input("Enter Grade (e.g., 10th, College): ").strip()

    while True: # Loop for GPA input validation
        try:
            gpa = float(input("Enter GPA (e.g., 3.5): "))
            if not 0.0 <= gpa <= 4.0: # Condition check
                 print("GPA must be between 0.0 and 4.0.")
                 continue
            break
        except ValueError: # Exception Handling
            print("Invalid input. Please enter a number for GPA.")
            
    new_student = Student(student_id, name, age, grade, gpa)
    students.append(new_student)
    print(f"\n✅ Student '{name}' added with ID: {student_id}")

def view_all_students(students):
    """Implements 'View all students' feature."""
    print("\n--- All Students Records ---")
    if not students:
        print("No student records found.")
        return
    
    print(f"ID: {'ID':<5} | Name: {'NAME':<20} | Age: {'AGE':<3} | Grade: {'GRADE':<5} | GPA: {'GPA':<4}")
    print("-" * 65)

    for student in students:
        print(student)
    print("-" * 65)

def students_search(students):
    """Implements 'Students search' feature."""
    query = input("\nEnter Student ID or Name to search: ").strip()
    if not query:
        return
    
    # Using a list comprehension for efficient searching
    found_students = [
        s for s in students 
        if query.lower() in s.id.lower() or query.lower() in s.name.lower() # Condition
    ]
    
    if found_students:
        print("\n--- Search Results ---")
        for student in found_students:
            print(student)
    else:
        print(f"No student found matching '{query}'.")

def update_and_delete(students):
    """Implements 'Update and Delete' feature."""
    student_id = input("\nEnter the ID of the student to Update or Delete: ").strip()
    
    try:
        # Finding the student using a generator expression
        student_to_modify = next(s for s in students if s.id == student_id)
    except StopIteration:
        print(f"Student with ID {student_id} not found.")
        return

    print("\n--- Student Found ---")
    print(student_to_modify)
    
    action = input("\nEnter action (U for Update / D for Delete): ").strip().upper()

    if action == 'D': # Condition for deletion
        students.remove(student_to_modify)
        print(f"✅ Student ID {student_id} ({student_to_modify.name}) has been **DELETED**.")
        
    elif action == 'U': # Condition for update
        print("\n--- Update Student Details --- (Press Enter to keep current value)")
        # ... (Input loops and exception handling for update similar to add function)
        
        # Name Update
        new_name = input(f"New Name ({student_to_modify.name}): ").strip()
        if new_name:
            student_to_modify.name = new_name

        # Age Update with validation (Exception Handling)
        while True:
            new_age = input(f"New Age ({student_to_modify.age}): ").strip()
            if not new_age: break
            try:
                new_age = int(new_age)
                if new_age > 0:
                    student_to_modify.age = new_age
                    break
                else: print("Age must be a positive number.")
            except ValueError: print("Invalid input. Please enter a number for Age.")

        # Grade Update
        new_grade = input(f"New Grade ({student_to_modify.grade}): ").strip()
        if new_grade:
            student_to_modify.grade = new_grade
            
        # GPA Update with validation (Exception Handling)
        while True:
            new_gpa = input(f"New GPA ({student_to_modify.gpa:.2f}): ").strip()
            if not new_gpa: break
            try:
                new_gpa = float(new_gpa)
                if 0.0 <= new_gpa <= 4.0: # Condition
                    student_to_modify.gpa = new_gpa
                    break
                else: print("GPA must be between 0.0 and 4.0.")
            except ValueError: print("Invalid input. Please enter a number for GPA.")

        print(f"✅ Student ID {student_id} ({student_to_modify.name}) has been **UPDATED**.")
        
    else:
        print("Invalid action. Operation cancelled.")

def calculate_avg_and_topper(students):
    """Implements 'Calculate avg & find topper' feature."""
    if not students: # Condition
        print("\nNo student records available for calculation.")
        return

    # Using a generator expression and sum() for efficient average calculation
    total_gpa = sum(s.gpa for s in students)
    average_gpa = total_gpa / len(students)
    
    # Finding the topper using max() with a key
    topper = max(students, key=lambda s: s.gpa)

    print("\n--- Calculation Summary ---")
    print(f"Total number of students: {len(students)}")
    print(f"Average GPA: {average_gpa:.2f}")
    
    print("\n🥇 Topper Found (Highest GPA) 🥇")
    print(topper)
    print("-" * 65)


# --- Main Application Loop ---

def main():
    """The main function to run the Student Management System."""
    students = load_students()
    
    while True: # Main application loop
        print("\n==============================================")
        print("    STUDENT MANAGEMENT SYSTEM (using Python)")
        print("==============================================")
        print("1. New Student - Add")
        print("2. View all students")
        print("3. Students search (by ID or Name)")
        print("4. Update and Delete")
        print("5. Calculate Avg GPA & Find Topper")
        print("6. Exit & Save")
        print("----------------------------------------------")

        choice = input("Enter your choice (1-6): ").strip()

        # Conditional execution based on user input
        if choice == '1':
            add_new_student(students)
        elif choice == '2':
            view_all_students(students)
        elif choice == '3':
            students_search(students)
        elif choice == '4':
            update_and_delete(students)
        elif choice == '5':
            calculate_avg_and_topper(students)
        elif choice == '6':
            save_students(students)
            print("👋 Thank you for using the Student Management System. Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please enter a number between 1 and 6.")
            
# Execute the main function
if __name__ == "__main__":
    main()