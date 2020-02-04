"""Triangle Class"""
# Thisara Wijesundera
# CS 351
# Triangle class

import math
from shape import Shape

class Triangle(Shape):
    """Triangle class"""

    def __init__(self, sides):
        Shape.__init__(self, sides)

    def __name__(self) -> str:
        return "Triangle"

    def area(self) -> float:
        """Find area using Herons formula

            Returns:
                area: Area of triangle given 3 sides

            Note:
                semiperimeter = Add all sides together, divide by 2
                Formula = sqrt(semi(semi-side1)(semi-side2)(semi-side3))
        """
        area = 0
        semi = 0

        semi += sum((side for side in self.sides)) / 2
        multiplication = (semi*(semi-self.sides[0])*(semi-self.sides[1])*(semi-self.sides[2]))

        area = round(math.sqrt(multiplication), 2)

        return area
