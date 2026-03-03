"""
Project: Course Lookup System
Language: Python
Concepts Demonstrated:
- Dictionaries
- Input normalization
- Conditional logic
- Structured program execution
- User interaction handling

Objective:
Provide course details (room, instructor, time)
based on user-entered course codes.
"""

def main():

    # Data mappings
    rooms_for_class = {
        "CS101": "3004",
        "CS102": "4501",
        "CS103": "6755",
        "NT110": "1244",
        "CM241": "1411"
    }

    teacher_for_class = {
        "CS101": "Haynes",
        "CS102": "Alvarado",
        "CS103": "Rich",
        "NT110": "Burke",
        "CM241": "Lee"
    }

    time_for_class = {
        "CS101": "8:00 a.m.",
        "CS102": "9:00 a.m.",
        "CS103": "10:00 a.m.",
        "NT110": "11:00 a.m.",
        "CM241": "1:00 p.m."
    }

    print("Course Lookup Program")
    course_guess = input("Enter a course number (e.g., CS101): ")

    course_guess = course_guess.strip().upper()

    if course_guess in rooms_for_class:
        print("\nCourse Details")
        print("-------------------")
        print("Room:     ", rooms_for_class[course_guess])
        print("Teacher:  ", teacher_for_class[course_guess])
        print("Time:     ", time_for_class[course_guess])
    else:
        available = ", ".join(sorted(rooms_for_class.keys()))
        print(f"\nCourse '{course_guess}' not found.")
        print("Available courses:", available)


if __name__ == "__main__":
    main()
