import unittest
import cmath
from math import isclose
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

    @given(floats(allow_nan=False, allow_infinity=False), floats(min_value=0.0001, max_value=10000))
    def test_nroot(self, total, n):
        """Test the nroot method."""

        self.calc.total = total

        try:
            result = self.calc.nroot(n)
            if total < 0 and n % 2 == 0:
                self.fail("Expected ValueError: Cannot compute even root of a negative number")
            elif n <= 0:
                self.fail("Expected ValueError: Index for nth root must be a positive number")
            else:
                if total == 0:
                    expected_result = 0
                else:
                    expected_result = cmath.exp(cmath.log(total) / n).real

            if isinstance(result, complex):
                result = result.real
            if isinstance(expected_result, complex):
                expected_result = expected_result.real

            self.assertTrue(isclose(result, expected_result, rel_tol=1e-5, abs_tol=1e-5))
            
        except ValueError as e:
            if total < 0 and not n % 2:
                self.assertEqual(str(e), "Cannot compute even root of a negative number")
            elif n <= 0:
                self.assertEqual(str(e), "Index for nth root must be a positive number")
            else:
                self.fail(f"Unexpected ValueError: {e}")

        except OverflowError as e:
            self.assertEqual(str(e), "Result too large to compute")

    def test_reset(self):
        """Test the reset method."""
        self.calc.total = 100
        self.assertEqual(self.calc.reset(), 0.0)

if __name__ == '__main__':
    unittest.main()
