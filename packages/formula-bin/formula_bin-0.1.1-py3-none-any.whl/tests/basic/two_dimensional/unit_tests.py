import unittest
from formulas.basic.two_dimensional import circle, rectangle, square, trapezoid, triangle


class TestTwoDimensional(unittest.TestCase):
    def test_circle(self):
        self.assertEqual(circle.area(44.678), 6271.007501310993)
        self.assertEqual(circle.circumference(34.67), 217.83803459991626)

    def test_rectangle(self):
        self.assertEqual(rectangle.area(32.5, 44.6), 1449.5)
        self.assertEqual(rectangle.perimeter(32.5, 44.6), 154.2)

    def test_square(self):
        self.assertEqual(square.area(12.5), 156.25)
        self.assertEqual(square.perimeter(12.5), 50.0)

    def test_trapezoid(self):
        self.assertEqual(trapezoid.area(
            13.67, 44.76, 34.8), 1016.6819999999999)

    def test_triangle(self):
        self.assertEqual(triangle.area(12.5, 33.8), 211.24999999999997)


if __name__ == '__main__':
    unittest.main()
