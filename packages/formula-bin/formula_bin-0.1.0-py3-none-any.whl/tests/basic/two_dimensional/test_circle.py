from formulas.basic.two_dimensional import circle


def test_area_circle():
    assert circle.area(44.678) == 6271.007501310993


def test_circumference():
    assert circle.circumference(34.67) == 217.83803459991626