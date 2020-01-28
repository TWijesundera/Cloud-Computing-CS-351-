"""
	Determine Status program Chapter 6
	CS 351
	Thisara Wijesundera
"""

try:
	user_input = input("Enter an age as a number \n")
	user_input = int(user_input)
	
	if user_input >= 0 and user_input <= 17:
		print("\nChild")
	elif user_input >= 18 and user_input <= 64:
		print("\nAdult")
	else:
		print("\nSenior")
	
	input("Press Enter to Exit")
except ValueError:
	print("\nPlease enter an integer value\n")
	quit()