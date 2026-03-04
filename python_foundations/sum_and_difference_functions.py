# ------------------------------------------------------------
# File: sum_and_difference_functions.py
# Date: Sept 24, 2025
# Author: Khia1
#
# Description:
# This script demonstrates how functions can be used to perform
# arithmetic operations. The program calculates:
#   1. The sum of two numbers
#   2. The difference between that sum and a third number
#
# The program runs several predefined test cases to illustrate
# how functions return values and how results can be reused.
# ------------------------------------------------------------


# ------------------------------------------------------------
# Function: find_sum
# Purpose:
#   Calculates the sum of two numbers and prints the result.
#
# Parameters:
#   num1 (int or float) : first number
#   num2 (int or float) : second number
#
# Returns:
#   total (int or float) : sum of num1 and num2
# ------------------------------------------------------------
def find_sum(num1, num2):

    total = num1 + num2

    print(f"Inside the function, the sum is: {total}")
    print(f"The sum of {num1} and {num2} is {total}")

    return total


# ------------------------------------------------------------
# Function: find_difference
# Purpose:
#   Calculates the difference between a previously computed sum
#   and a third number.
#
# Parameters:
#   sum_value (int or float) : result returned from find_sum
#   num3 (int or float)      : number to subtract
#
# Returns:
#   difference (int or float) : result of subtraction
# ------------------------------------------------------------
def find_difference(sum_value, num3):

    difference = sum_value - num3

    print(f"Inside the function, the difference is: {difference}")
    print(f"The difference between {sum_value} and {num3} is {difference}")

    return difference


# ------------------------------------------------------------
# Test Cases
# These examples demonstrate how the functions behave with
# different input values.
# ------------------------------------------------------------

test_cases = [
    (20, 15, 10),
    (50, 25, 10),
    (75, 50, 30),
    (100, 30, 50)
]


# ------------------------------------------------------------
# Run the test cases
# ------------------------------------------------------------
for num1, num2, num3 in test_cases:

    sum_result = find_sum(num1, num2)
    diff_result = find_difference(sum_result, num3)

    print(f"The original numbers are: {num1} and {num2}")
    print()
