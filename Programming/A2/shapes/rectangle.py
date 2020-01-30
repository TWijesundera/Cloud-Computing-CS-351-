"""Rectangle Class"""
# Thisara Wijesundera
# CS 351
# Rectangle Class

from shape import Shape

class Rectangle(Shape):
    """Rectangle class
        Args:
        Returns:
    """

    def __init__(self, sides):
        Shape.__init__(self, sides)

    def __name__(self) -> str:
        return "Rectangle"

    def area(self) -> int:
        """The area is defined by the parent method"""
        return Shape.area(self)
