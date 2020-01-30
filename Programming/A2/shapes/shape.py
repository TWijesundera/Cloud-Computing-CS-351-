"""Parent class to rectangle and triangle"""
# Thisara Wijesundera
# CS 351
# Shape class

from typing import List

class Shape:
    """Shape class

        Parent class for Rectangle and Triangle

        Args:

        Returns:
    """
    def __init__(self, sides: List[int]):
        self.sides = sides
    
    def __name__(self):
        return "Shape"

    def __repr__(self):
        return self.__name__(), self.sides

    def __str__(self):
        return "{} with sides {}".format(self.__name__(), str(self.sides)[1:-1])

    def area(self) -> int:
        """Returns the area of a shape

            Multiplies all side together in self.sides

            Args:
                None
            Returns:
                area(int): The multiplcation of all sides
        """
        area = 0
        for side in range(len(self.sides)-1):
            area += self.sides[side] * self.sides[side+1]
        return area

def parse_input(input_file: str) -> List[Shape]:
    """Parses the input from a given file
        
        Opens file, splits the line and changes the sides to int's
            then creates an object

        Args:
            input_file (str): Path to file
        Returns:
            output (List[shape]): A list of shape objects
    """
    output = []
    with open(input_file) as file:
        for line in file:
            splited = line.split()
            sides = [int(x) for x in splited[1:]]
            if splited[0] == 'T':
                output.append(Triangle(sides))
            else:
                output.append(Rectangle(sides))
    return output

if __name__ == "__main__":
    import sys
    from rectangle import Rectangle
    from triangle import Triangle

    try:
        if len(sys.argv) != 2:
            raise ValueError("\nPlease make sure you provide the input txt file\n")
        shapes = parse_input(sys.argv[1])
        print("\n----------Areas----------\n")

        for shape in shapes:
            print("{}: Area = {}".format(shape.__str__(), shape.area()))

    except ValueError as err:
        print(err)
    