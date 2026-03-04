# number_range_checker.py
# Author: KHia1
# Purpose:
# This script defines a function that checks whether a number falls
# within the range from 1 to 100. It then tests the function using
# several example numbers and prints the results.

def the_numbers_range(num):
    """
    Check whether a number is between 1 and 100.

    Parameters
    ----------
    num : int or float
        The number to evaluate.

    Returns
    -------
    bool
        True if the number is within the range [1, 100],
        otherwise False.
    """

    # Check if the number is inside the allowed range
    if num >= 1 and num <= 100:
        print("The number is within the range")
        return True
    else:
        print("The number is outside the range")
        return False


# List of numbers used to test the function
tries = [50, 200, -5, 100, 0]

# Loop through each number and evaluate it
for n in tries:
    print("For num as", n)

    # Call the function and store the result
    result = the_numbers_range(n)

    # Print the returned value (True or False)
    print(result, "was returned")

    # Add spacing between results to improve readability
    print()
