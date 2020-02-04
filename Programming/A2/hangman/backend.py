"""The backend of the hangman program"""
# Thisara Wijesundera
# CS 351
# Hangman Game

from typing import List

__guessed_letters = list()
__num_guesses = 6
__player_score = 0

def add_to_guessed(letter: str):
    """Adds the letter the user guessed to a list"""
    __guessed_letters.append(letter)

def used_letters() -> List[str]:
    """Returns the letters the user guessed"""
    return __guessed_letters

def get_score() -> int:
    """Gets the players score"""
    return __player_score

def get_guesses() -> int:
    """Get the number of guesses the user has left"""
    return __num_guesses

def add_score(score: int):
    """Adds the arg score to the players current score"""
    global __player_score
    __player_score += score

def subtract_score(score: int):
    """Subtracts the arg score from the players current score"""
    global __player_score
    __player_score -= score

def subtract_guess():
    """Subtracts a guess from the users guesses"""
    global __num_guesses
    __num_guesses -= 1 

def reset_guesses():
    """Resets the number of guesses available to the user back to 6"""
    global __num_guesses
    __num_guesses = 6

def clear_guessed_letters():
    """Clears the list of guessed letters"""
    global __guessed_letters
    __guessed_letters.clear()

def check_if_guessed(current_guess: str) -> bool:
    """Checks if the user guessed the random word correctly"""
    return current_guess.count('-') == 0