from formulas.basic.three_dimensional import cylinder


def test_curved_surface_area():
    assert cylinder.curved_surface_area(34.78, 67.9) == 14838.13166039364


def test_surface_area():
    assert cylinder.surface_area(65.78, 44.33) == 45509.33611793574


def test_volume():
    assert cylinder.volume(56.897, 34.879) == 354725.68309774617
