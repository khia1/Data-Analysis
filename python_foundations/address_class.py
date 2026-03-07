"""
address_class.py
Author: Kia

Purpose
-------
Demonstrates a simple Object-Oriented Programming (OOP) design in Python.

This module defines an Address class capable of:
- storing address information
- printing the address in a formatted way
- comparing two addresses by ZIP code

Concepts demonstrated
---------------------
- class design
- constructors (__init__)
- instance attributes
- optional parameters
- class methods
- object comparison
"""


class Address:
    """
    Represents a postal address.

    Attributes
    ----------
    num : int or str
        Street number

    road : str
        Street name

    city : str
        City name

    state : str
        State abbreviation

    zip_code : str
        Postal code stored as string for consistency

    suite : str or None
        Optional suite or unit number
    """

    def __init__(self, num, road, city, state, zip_code, suite=None):
        """
        Initialize an Address object.

        Parameters
        ----------
        num : int or str
            Street number

        road : str
            Street name

        city : str
            City name

        state : str
            State abbreviation

        zip_code : int or str
            ZIP / postal code

        suite : str, optional
            Suite or unit number (default is None)
        """

        self.num = num
        self.road = road
        self.city = city
        self.state = state

        # Convert zip to string to ensure consistent formatting
        self.zip_code = str(zip_code)

        self.suite = suite

    def show(self):
        """
        Print the address in a standard two-line format.
        """

        if self.suite:
            print(f"{self.num} {self.road}, Suite {self.suite}")
        else:
            print(f"{self.num} {self.road}")

        print(f"{self.city}, {self.state} {self.zip_code}")

    def zip_comes_first(self, other):
        """
        Compare ZIP codes between two Address objects.

        Parameters
        ----------
        other : Address
            Another Address object to compare against

        Returns
        -------
        bool
            True if this address has a smaller ZIP code
        """

        return int(self.zip_code) < int(other.zip_code)


# -------------------------------------------------
# Example usage
# -------------------------------------------------
if __name__ == "__main__":

    # Create two address objects
    address1 = Address(
        1200,
        "Market Street",
        "San Francisco",
        "CA",
        94103
    )

    address2 = Address(
        500,
        "Broadway",
        "New York",
        "NY",
        10012,
        suite="8B"
    )

    print("Address 1")
    address1.show()

    print("\nAddress 2")
    address2.show()

    # Compare ZIP codes
    print("\nZIP comparison")
    if address1.zip_comes_first(address2):
        print("Address 1 comes first by ZIP code.")
    else:
        print("Address 2 comes first by ZIP code.")
