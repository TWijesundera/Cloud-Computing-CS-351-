"""Module handles the games printing"""
# Thisara Wijesundera
# CS 351
# Hangman Game

from backend import used_letters, clear_guessed_letters, reset_guesses
from dictionary import remove_from_choices

def print_game(word: str) -> str:
    """Creates the current guess string"""
    letters = used_letters()
    return "".join(['-' if char not in letters else f'{char}' for char in word])

def print_guessed_letters() -> str:
    """Prints the letters the user has already guessed"""
    return " ".join(used_letters())

def game_cleanup(guess_word: str):
    """Common clean up for the end of a game

        Removes the guessed word from the dictionary
        Clears the guessed letters
        Resets the amount of guesses the user has
    """
    remove_from_choices(guess_word)
    clear_guessed_letters()
    reset_guesses()
