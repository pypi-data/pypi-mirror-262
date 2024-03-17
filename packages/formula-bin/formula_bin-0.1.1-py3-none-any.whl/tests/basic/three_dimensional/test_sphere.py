from formulas.basic.three_dimensional import sphere


def test_surface_area():
    assert sphere.surface_area(3.9) == 191.134497044403


def test_volume():
    assert sphere.volume(3.9) == 248.47484615772387

