import unittest
from formulas.basic.two_dimensional import circle, rectangle


class TestTwoDimensional(unittest.TestCase):
    def test_circle(self):
        self.assertEqual(circle.area(44.678), 6271.007501310993)
        self.assertEqual(circle.circumference(34.67), 217.83803459991626)

    def test_rectangle(self):
        self.assertEqual(rectangle.area(32.5, 44.6), 1449.5)
        self.assertEqual(rectangle.perimeter(32.5, 44.6), 154.2)


if __name__ == '__main__':
    unittest.main()
