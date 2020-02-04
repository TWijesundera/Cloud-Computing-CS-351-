"""Dictionary module

    This module uses the dictionary to parse the file
        and pick a new word
"""
# Thisara Wijesundera
# CS 351
# Hangman Game

import random

hangman_words = dict()

def parse_file(path_to_file: str):
    """Parses the dictionary file the user provides"""
    with open(path_to_file) as in_file:
        """
            For every line in the file find the word and score
            Then palce it in the dict of potential words
        """
        for line in in_file:
            splited = line.split()
            hangman_words[splited[0]] = int(splited[1])

def choose_word() -> str:
    """Chooses a random word from the dictionary"""
    return random.choice(list(hangman_words))

def remove_from_choices(guessed: str):
    """Removes the provided arg from the dictionary"""
    hangman_words.pop(guessed, None)
