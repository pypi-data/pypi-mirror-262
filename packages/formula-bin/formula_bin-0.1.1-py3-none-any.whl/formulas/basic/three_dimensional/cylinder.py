from math import pi


# Curved surface area of the cylinder
def curved_surface_area(radius, height):
    """
    :param radius: radius of base of Cylinder
    :param height: height of Cylinder
    :return: curved surface area of the cylinder
    """
    return 2.0 * pi * radius * height


# Total surface area of the cylinder
def surface_area(radius, height):
    """
    :param radius: radius of base of Cylinder
    :param height: height of Cylinder
    :return: surface area of the Cylinder
    """
    return 2.0 * pi * radius * (radius + height)


# Volume of the cylinder
def volume(radius, height):
    """
    :param radius: radius of base of Cylinder
    :param height: height of Cylinder
    :return: Volume of the cylinder
    """
    return pi * (radius ** 2) * height
