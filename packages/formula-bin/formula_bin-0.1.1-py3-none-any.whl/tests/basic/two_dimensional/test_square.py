from formulas.basic.two_dimensional import square


def test_square_area():
    assert square.area(12.5) == 156.25


def test_square_perimeter():
    assert square.perimeter(12.5) == 50.0
