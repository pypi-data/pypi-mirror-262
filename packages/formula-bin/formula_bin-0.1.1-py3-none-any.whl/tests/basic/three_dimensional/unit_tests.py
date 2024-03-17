import unittest
from formulas.basic.three_dimensional import cone, cube, cylinder, sphere


class TestThreeDimensional(unittest.TestCase):
    def test_cone(self):
        self.assertEqual(cone.curved_surface_area(
            12.89, 56.9), 2304.1728574415515)
        self.assertEqual(cone.surface_area_with_curved_length(
            45.87, 33.98), 11506.772673360078)
        self.assertEqual(cone.surface_area_of_cone_without_curved_length(
            32.90, 11.34), 6997.312479572007)
        self.assertEqual(cone.volume(
            21.8, 33.33), 16587.346573808267)

    def test_cube(self):
        self.assertEqual(cube.surface_area(33.89), 6891.1926)
        self.assertEqual(cube.volume(87.56), 671300.9452160001)

    def test_cylinder(self):
        self.assertEqual(cylinder.curved_surface_area(
            34.78, 67.9), 14838.13166039364)
        self.assertEqual(cylinder.surface_area(
            65.78, 44.33), 45509.33611793574)
        self.assertEqual(cylinder.volume(
            56.897, 34.879), 354725.68309774617)

    def test_sphere(self):
        self.assertEqual(sphere.surface_area(3.9), 191.134497044403)
        self.assertEqual(sphere.volume(3.9), 248.47484615772387)


if __name__ == "__main__":
    unittest.main()
