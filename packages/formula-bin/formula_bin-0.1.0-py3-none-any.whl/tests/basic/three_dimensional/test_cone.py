from formulas.basic.three_dimensional import cone


def test_curved_surface_area():
    assert cone.curved_surface_area(
        12.89, 56.9) == 2304.1728574415515


def test_surface_area_with_curved_length():
    assert cone.surface_area_with_curved_length(
        45.87, 33.98) == 11506.772673360078


def test_surface_area_without_curved_length():
    assert cone.surface_area_of_cone_without_curved_length(
        32.90, 11.34) == 6997.312479572007


def test_volume():
    assert cone.volume(
        21.8, 33.33) == 16587.346573808267
