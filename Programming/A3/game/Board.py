"""This class handles all interations with the
    tic tac toe board

    Requirements:
        Python 3.6: There are uses of f strings in this code

    Author: Thisara Wijesundera
    CS 351
    Assignment 3

    Future Improvements:
        Create an interactive GUI for the user
"""
import sys

from typing import Dict

class Board:
    """ Class that holds all functions for the tic tac toe board

        Instance Variables:
            _board (list): A double 2D list holding the tic tac toe board
    """

    def __init__(self):
        """Initializes an empty 9x9 board into a dict

            Instance:
                _board (Dict): stores the entire tic tac toe
                    board into a 9x9 dict for quick access

            Improvements:
                Only initialize locations like (2,3) (4,6) etc
                    to save space. Handle the empty spaces in printing
        """
        self._board = {key: ['-'] * 9 for key in range(9)}

    def update_board(self, row: int, col: int, symbol: str):
        """Updates self._board to reflect the symbol placed

            Args:
                row (int): Row to place symbol
                col (int): Column to place symbol
                symbol (str): An 'X' or an 'O'

            Returns:
                None
        """
        if 1 <= row <= 9 and 1 <= col <= 9:
            location_to_change = self._board[row-1][col-1]
            if location_to_change == '-':
                self._board[row-1][col-1] = symbol
            else:
                raise IndexError("There is already a symbol in that position\n")
        else:
            raise IndexError("Unable to access that location\n")

    def board_full(self) -> bool:
        """Check if the board is full

            Returns:
                True: The board is completely full
                False: The board still has empty spaces
        """
        for row in self._board.values():
            if '-' in row:
                return False
        return True

    def find_winner(self) -> str:
        """Checks if there is 3 in a row on the horizontal
           vertical and diagonal

            Returns:
                The winners symbol or None if there is no winner

            Future Improvements:
                Instead we could get the row that was just added to
                and check the row before and after for a winner in a 3x3 area

        """
        vertical = self.check_vertical()
        horizontal = self.check_horizontal()
        diagonal = self.check_diagonal()

        if vertical[0]:
            return vertical[1]
        if horizontal[0]:
            return horizontal[1]
        if diagonal[0]:
            return diagonal[1]
        return None

    def check_horizontal(self) -> tuple:
        """Checks each row for 3 in a row

            Returns:
                True: If 3 in a row is found
                False: If 3 in a row is not found on the board
        """
        for row in self._board.values():
            for index in range(len(row)-2):
                if row[index] != '-':
                    # print(f"first: {row[index]} second: {row[index+1]} third: {row[index+2]}")
                    if row[index] == row[index+1] == row[index+2]:
                        return (True, row[index])
            return (False, None)

    def check_vertical(self) -> tuple:
        """Checks for 3 in a row vertically

            Retuns:
                True, symbol: If 3 in a row in found
                False, none: If 3 in a row is not found
        """
        ref_board = self._board
        for key in range(len(ref_board)-2):
            for index in range(len(ref_board[key])):
                if ref_board[key][index] != '-':
                    if ref_board[key][index] == ref_board[key+1][index] \
                       == ref_board[key+2][index]:
                        return (True, ref_board[key][index])
        return (False, None)

    def check_diagonal(self) -> tuple:
        """Checks for 3 in a row diagonally

            Returns:
                True: If 3 in a row is found
                False: If 3 in a row is not found
        """
        ref_board = self._board
        for key in range(len(ref_board)-2):
            for index in range(len(ref_board[key])-2):
                if ref_board[key][index] != '-':
                    if ref_board[key][index] == ref_board[key+1][index+1] \
                        == ref_board[key+2][index+2]:
                        return (True, ref_board[key][index])
        return (False, None)

    def __repr__(self) -> Dict:
        """Returns the dictionary"""
        return self._board

    def __str__(self) -> str:
        """Prints the board in a string format

            Return:
                printed_board (str): String represenation of the board
        """
        printed_board = []
        printed_board.append("ROW")
        for row_num, row in reversed(list(enumerate(self._board))):
            printed_board.append("  {}  {}".format(row_num+1, "  ".join(self._board[row_num])))
        printed_board.append("COL  {}".format("  ".join([str(x+1) for x in range(len(self._board))])))
        return "\n".join(printed_board)

if __name__ == "__main__":
    print("Please run using Server.py\n")
    sys.exit()
