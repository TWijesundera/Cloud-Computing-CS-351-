"""
    Thisara Wijesundera
    CS 351

    Description:
        Print a phrase to the user depending on 
        if there are less or more than 3 arguments provided
"""
import sys

print("There are 3 or more arguments") if len(sys.argv) >= 3 else print("There are less than 3 arguments")