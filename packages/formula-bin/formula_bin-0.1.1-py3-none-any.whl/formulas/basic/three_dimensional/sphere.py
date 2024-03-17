from math import pi, pow


def surface_area(radius):
    """
    Surface area of the cube.
    Sphere should be a perfect one.
    :param radius: radius of the sphere
    :return: Surface area of the sphere.
    """
    return 4.0 * pi * pow(radius, 2)


def volume(radius):
    """
    Volume of a sphere.
    Sphere should be a perfect one.
    :param radius: radius of the sphere
    :return: Volume of the sphere
    """
    return (4.0 / 3.0) * (pi * pow(radius, 3))
