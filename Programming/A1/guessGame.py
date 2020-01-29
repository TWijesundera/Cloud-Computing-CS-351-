# CS 351 
# Thisara Wijesundera
# Guess Game for Chapter 7 & 8

import random

num_to_guess = random.choice(range(5, 16))
num_guesses = 1

try:
	user_guess = int(input("I'm thinking of a number between 5 and 15\n"))

	""" Keep gussing until the user guesses the number stored in num_to_guess """
	while user_guess != num_to_guess:
		print(num_to_guess - user_guess)
		if int(num_to_guess - user_guess) <= 3:
			print("\nHOT")
		else:
			print("\nCOLD")

		user_guess = int(input("\nGuess another number\n"))
		num_guesses += 1

	print("\nMATCH. The number of guesses was: {}".format(num_guesses))
	
except ValueError:
	print("You entered something other than an integer")
	user_input = input("\nTry guessing a different number \n")