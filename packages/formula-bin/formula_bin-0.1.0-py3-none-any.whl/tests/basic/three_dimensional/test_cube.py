from formulas.basic.three_dimensional import cube


def test_surface_area():
    assert cube.surface_area(33.89) == 6891.1926


def test_volume():
    assert cube.volume(87.56) == 671300.9452160001
