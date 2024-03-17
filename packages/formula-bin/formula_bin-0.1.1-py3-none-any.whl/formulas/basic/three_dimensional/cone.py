from math import pi, sqrt


# Curved surface area of cone
def curved_surface_area(radius, curved_length):
    """
    Function to calculate curved surface area of cone.
    Cone should be equilateral
    :param radius: radius of the cone
    :param curved_length: curved length of cone.
    :return: curved surface area
    """
    return pi * radius * curved_length


# Total surface area of cone
def surface_area_with_curved_length(radius, curved_length):
    """
    Function to calculate area of cone with curved length
    cone should be equilateral. This function doesn't need height
    :param radius: radius if cone
    :param curved_length: curved length of cone
    :return: surface area of cone with radius and curved length
    """
    return pi * radius * (radius + curved_length)


def surface_area_of_cone_without_curved_length(radius, height):
    """
    Function to calculate surface area of cone with radius and height
    cane should be equilateral. This function doesn't need curved length.
    :param radius: radius of the cone
    :param height: height of the cone
    :return: surface area of cone without curved length
    """
    return pi * radius * (radius + sqrt(height ** 2 + radius ** 2))


# Volume of cone
def volume(radius, height):
    """
    Function to calculate volume of cone
    :param radius: radius of cone
    :param height: height of cone
    :return: volume of cone
    """
    return (1.0 / 3.0) * pi * (radius ** 2) * height
