import unittest
from hypothesis import given
from hypothesis.strategies import floats
from calculator_mfelic import Calculator

class TestCalculator(unittest.TestCase):
    """Test class for the Calculator."""

    def setUp(self):
        """Create a new Calculator object before each test."""
        self.calc = Calculator()

    @given(floats(allow_nan=False, allow_infinity=False))
    def test_add(self, num):
        """Test the add method."""
        expected = self.calc.total + num
        self.assertAlmostEqual(self.calc.add(num), expected)

    @given(floats(allow_nan=False, allow_infinity=False))
    def test_sub(self, num):
        """Test the sub method."""
        expected = self.calc.total - num
        self.assertAlmostEqual(self.calc.sub(num), expected)

    @given(floats(allow_nan=False, allow_infinity=False))
    def test_mult(self, num):
        """Test the mult method."""
        expected = self.calc.total * num
        self.assertAlmostEqual(self.calc.mult(num), expected)


    @given(floats(allow_nan=False, allow_infinity=False), floats(allow_nan=False, allow_infinity=False, min_value=1e-6, max_value=1e6))
    def test_div(self, total, divisor):
        """Test the div method."""
        self.calc.total = total
        if divisor != 0:
            expected = total / divisor
            self.assertAlmostEqual(self.calc.div(divisor), expected)
        else:
            with self.assertRaises(ZeroDivisionError):
                self.calc.div(divisor)

    @given(floats(min_value=0, max_value=10000), floats(min_value=0.1, max_value=10000))
    def test_nroot(self, total, n):
        self.calc.total = total
        expected = total ** (1 / n)
        self.assertAlmostEqual(self.calc.nroot(n), expected)

    def test_reset(self):
        """Test the reset method."""
        self.calc.total = 100
        self.assertEqual(self.calc.reset(), 0.0)

if __name__ == '__main__':
    unittest.main()
