from formulas.basic.two_dimensional import rectangle


def test_rectangle_perimeter():
    assert rectangle.perimeter(32.5, 44.6) == 154.2


def test_rectangle_area():
    assert rectangle.area(32.5, 44.6) == 1449.5