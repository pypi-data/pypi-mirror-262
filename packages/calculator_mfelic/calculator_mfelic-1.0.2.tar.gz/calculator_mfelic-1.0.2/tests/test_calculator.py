import unittest
from calculator_mfelic import Calculator

class TestCalculator(unittest.TestCase):

    def setUp(self):
        # Create a new instance of Calculator before each test
        self.calc = Calculator()

    def test_add(self):
        self.calc.add(5)
        self.assertEqual(self.calc.total, 5)

    def test_sub(self):
        self.calc.sub(3)
        self.assertEqual(self.calc.total, -3)

    def test_mult(self):
        self.calc.add(2)
        self.calc.mult(3)
        self.assertEqual(self.calc.total, 6)

    def test_div(self):
        self.calc.add(10)
        self.calc.div(2)
        self.assertEqual(self.calc.total, 5)

    def test_nroot(self):
        self.calc.add(8)
        self.calc.nroot(3)
        self.assertAlmostEqual(self.calc.total, 2.0)  # Due to floating point precision, use assertAlmostEqual for approximate comparison

    def test_reset(self):
        self.calc.add(10)
        self.calc.reset()
        self.assertEqual(self.calc.total, 0.0)

if __name__ == '__main__':
    unittest.main()