# number_guessing_game.py
# Author: KHIA1
#
# Purpose:
# This program is a simple number guessing game.
# The computer randomly selects a number between 1 and 25.
# The player has four attempts to guess the correct number.
# After each guess, the program provides feedback indicating
# whether the guess was too high or too low.


import random


# Generate a random number between 1 and 25
myRandom_number = random.randint(1, 25)


# Allow the player up to 4 attempts
for turn in range(1, 5):

    # Ask the player for a guess
    player_pick = int(input("Take a guess (1–25): "))

    # If the guess is correct, congratulate the player and stop the game
    if player_pick == myRandom_number:
        print(f"Congratulations! You nailed it in {turn} attempt(s).")
        break

    # If the guess is higher than the number
    elif player_pick > myRandom_number:
        print("Too high! Try again.")

    # If the guess is lower than the number
    else:
        print("Too low! Try again.")


# If the player did not guess the number within 4 attempts
else:
    print(f"Sorry, no more chances. The number was {myRandom_number}.")
