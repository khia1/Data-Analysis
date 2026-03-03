"""
Project: Employee Directory Data Model
Language: Python
Concepts Demonstrated:
- Dictionaries
- Lists
- Data aggregation
- Iteration and filtering
- Basic data retrieval logic

Objective:
Model a simple employee directory using Python data structures.
"""

# -------------------------------
# Data Initialization
# -------------------------------

employees = [
    {"name": "John McKee", "age": 38, "department": "Sales"},
    {"name": "Lisa Crawford", "age": 29, "department": "Marketing"},
    {"name": "Sujan Patel", "age": 33, "department": "HR"},
]


# -------------------------------
# Directory Display
# -------------------------------

def display_directory(data):
    print("--------- Employee Directory ---------")
    for person in data:
        print(
            f"Name: {person['name']} | "
            f"Age: {person['age']} | "
            f"Department: {person['department']}"
        )


# -------------------------------
# Employee Lookup
# -------------------------------

def find_employee_by_name(data, target_name):
    for person in data:
        if person["name"] == target_name:
            return person
    return None


# -------------------------------
# Execution
# -------------------------------

if __name__ == "__main__":
    print("Raw Data Structure:\n")
    print(employees)
    print()

    display_directory(employees)

    print("\n--- Lookup Result: Sujan Patel ---")
    result = find_employee_by_name(employees, "Sujan Patel")

    if result:
        print(result)
    else:
        print("Employee not found.")
