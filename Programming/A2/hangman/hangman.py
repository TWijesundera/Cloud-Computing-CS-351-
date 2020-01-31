"""Driver Class for a Hangman game"""
# Thisara Wijesundera
# CS 351
# Hangman Game

import sys

from dictionary import parse_file, OUTPUT, choose_word, remove_from_choices
from printing import *
from backend import *

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            msg = ('\nPlease make sure to run the '
                   'program with the dictionary text file\n')
            raise ValueError(msg)

        parse_file(sys.argv[1])

        guess_word = choose_word()
        msg = ("I've picked a word from the provided dictionary."
               " You have 6 tries to guess the word.\n")
        print(msg)

        while get_score() < 1000 and get_score() >= 0:
            current_guess = print_game(guess_word)
            print("Current Guess: {} ".format(current_guess))
            print("User Letters: {}".format(print_guessed_letters()))
            print("Number of tries left: {}\n".format(get_guesses()))

            letter = input("\nPlease guess a letter: ")

            if len(letter) == 1 and letter.isalpha():
                if letter not in used_letters():
                    if letter in guess_word:
                        print("\nYes, there is a {}\n".format(letter))
                        add_to_guessed(letter)
                    else:
                        print("\nSorry, no {}".format(letter))
                        subtract_guess()
                        add_to_guessed(letter)
                else:
                    print("You've already guessed that letter!\n")

                if get_guesses() != 0:
                    if current_guess.count('-') <= 1:
                        add_score(OUTPUT[guess_word])
                        print("Congratulations! You won this round. Your current score is {}\n"
                              .format(get_score()))

                        game_cleanup(guess_word)
                        guess_word = choose_word()
                else:
                    subtract_score(OUTPUT[guess_word])
                    print("Sorry, the word I picked was '{}'. Your current score is {}\n"
                          .format(guess_word, get_score()))

                    game_cleanup(guess_word)
                    guess_word = choose_word()
            else:
                print("The chracter(s) you entered are invalid. Please try again.\n")

        WIN_MSG = "Your score is over 1000. You win!\n"
        LOSE_MSG = "Sorry, your score is negative. You lose\n"
        print(WIN_MSG) if get_score() > 1000 else print(LOSE_MSG)

    except ValueError as err:
        print(err)
    except KeyboardInterrupt:
        print('\n')
        sys.exit()
