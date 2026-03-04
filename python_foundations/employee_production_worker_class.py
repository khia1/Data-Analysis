# employee_production_worker_class.py
# Author: KHIA1
#
# Purpose:
# This script demonstrates object-oriented programming in Python.
# It defines a base class called Employee and a derived class called
# ProductionWorker. The ProductionWorker class inherits from Employee
# and adds information about work shift and hourly pay rate.
#
# The program then collects employee information from the user,
# creates a ProductionWorker object, and displays the stored data.


class Employee:
    """
    Base class representing a generic employee.
    Stores the employee's name and identification number.
    """

    def __init__(self, person_label, registry_code):
        # Internal attributes for employee identity
        self._person_label = person_label
        self._registry_code = registry_code

    # Accessor methods (getters)

    def get_name(self):
        """Return the employee's name."""
        return self._person_label

    def get_id(self):
        """Return the employee's identification number."""
        return self._registry_code

    # Mutator methods (setters)

    def set_name(self, updated_label):
        """Update the employee's name."""
        self._person_label = updated_label

    def set_id(self, updated_code):
        """Update the employee's identification number."""
        self._registry_code = updated_code


class ProductionWorker(Employee):
    """
    Derived class representing a production worker.
    Inherits basic employee information from Employee
    and adds shift assignment and hourly pay rate.
    """

    def __init__(self, person_label, registry_code, shift_tag, rate_per_hour):
        # Call the constructor of the parent class (Employee)
        super().__init__(person_label, registry_code)

        # Additional attributes specific to production workers
        self._shift_tag = shift_tag
        self._rate_per_hour = rate_per_hour

    # Accessor methods

    def get_shift(self):
        """Return the worker's shift assignment."""
        return self._shift_tag

    def get_pay_rate(self):
        """Return the worker's hourly pay rate."""
        return self._rate_per_hour

    # Mutator methods

    def set_shift(self, new_shift_tag):
        """Update the worker's shift assignment."""
        self._shift_tag = new_shift_tag

    def set_pay_rate(self, new_rate):
        """Update the worker's hourly pay rate."""
        self._rate_per_hour = new_rate


def main():
    """
    Main function that collects employee information,
    creates a ProductionWorker object, and prints the stored data.
    """

    print("Production unit record creation")

    # Collect employee information from the user
    entered_name = input("Name of employee: ")
    entered_number = input("Employee identification number: ")

    # Shift and hourly wage information
    shift_info = int(input("Shift assignment (1 = day, 2 = night): "))
    wage_info = float(input("Hourly compensation rate: "))

    # Create ProductionWorker object using the collected data
    worker_entry = ProductionWorker(
        entered_name,
        entered_number,
        shift_info,
        wage_info
    )

    # Display stored employee information
    print("\nStored profile")
    print("Recorded name:", worker_entry.get_name())
    print("Recorded number:", worker_entry.get_id())
    print("Assigned shift:", worker_entry.get_shift())
    print("Hourly rate:", worker_entry.get_pay_rate())


# Ensure the main function runs only when the script is executed directly
if __name__ == "__main__":
    main()
