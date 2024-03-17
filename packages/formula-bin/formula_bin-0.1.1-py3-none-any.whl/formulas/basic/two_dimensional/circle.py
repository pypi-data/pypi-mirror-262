# Find area of a Circle
from math import pi


def area(radius):
    """
        This function returns the area of circle with the provided input.

        Parameters:
        radius (float): Radius of a circle.

        Returns:
        float: area of the circle
    """
    return pi * (radius ** 2)


def circumference(radius):
    return 2 * pi * radius
