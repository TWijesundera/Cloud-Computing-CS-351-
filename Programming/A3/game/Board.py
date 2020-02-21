"""This class handles all interations with the
    tic tac toe board

    Author: Thisara Wijesundera
    CS 351
    Assignment 3
"""
from typing import List

class Board:
    """ Class that holds all functions for the tic tac toe board

        Instance Variables:
            _board (list): A double 2D list holding the tic tac toe board
    """

    def __init__(self):
        """Initializes an empty 9x9 board into a dict"""
        self._board = { key: ['-'] * 9 for key in range(9) }

    def update_board(self, row, col, symbol):
        """Updates self._board to reflect the symbol placed

            Args:
                row (int): Row to place symbol
                col (int): Column to place symbol
                symbol (str): An 'X' or an 'O'

            Returns:
                None
        """
        location_to_change = self._board[row-1][col-1]
        if location_to_change == '-':
            self._board[row-1][col-1] = symbol
        else:
            raise IndexError("There is already a symbol in that position\n")

    def board_full(self) -> bool:
        """Check if the board is full"""
        for x in self._board.values():
            if '-' in x:    
                return False
        return True

    def find_winner(self) -> str:
        """Checks if there is 3 in a row on the horizontal
           vertical and diagonal

            Args:

            Returns:
                The winners symbol

            Algorithm:
                If all return false then check if the board is filled
                If the board is filled then it is a draw
        
        """
        print("vertical: {}".format(self.check_vertical()))
        print("horizontal: {}".format(self.check_horizontal()))
        print("diagonal: {}".format(self.check_diagonal()))

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
            
            Algorithm:
                Loop the dictionary keys to the length of dict - 2
                to prevent index out of bounds error

                Loop over the row and find the first non '-' character
                Check if 
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

    def reset_board(self):
        pass

    def __repr__(self):
        """Returns the dictionary"""
        return self._board

    def __str__(self) -> str:
        """Prints the board in a string format
            
            Return:
                printed_board(str): String represenation of the board
        """
        printed_board = []
        printed_board.append("ROW")
        for row_num, row in enumerate(self._board):
            printed_board.append("  {}  {}".format(row_num+1, "  ".join(self._board[row_num])))
        printed_board.append("COL  {}".format("  ".join([str(x+1) for x in range(len(self._board))])))
        return "\n".join(printed_board)

if __name__ == "__main__":
    board = Board()
    board.update_board(1,7,'O')
    board.update_board(1,8,'O')
    board.update_board(1,9,'O')
    board.update_board(7,7,'O')
    board.update_board(8,8,'O')
    board.update_board(9,9,'O')
    print(board.__str__())
    board.find_winner()
    #print(board.board_full())
    """
    board.update_board(2, 3, 'X')
    print("\n")
    board.__str__()
    board.update_board(2, 3, 'X')
    print("\n")
    board.__str__()
    """