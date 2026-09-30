import unittest  # Use Python's built-in test runner and assertions.
# from streamlit.testing.v1 import AppTest  # Simulate the Streamlit interface (later lesson).
from calculator import divide, multiply, power  # Import the real backend functions.


class CalculatorTests(unittest.TestCase):  # Group backend behavior checks.
    def test_multiply(self):  # Check one ordinary multiplication.
        self.assertEqual(multiply(6, 4), 24)  # Six times four should be twenty-four.
        # for a, b, expected in [(6, 4, 24), (-3, 4, -12), (0, 7, 0), (1.5, 2, 3)]:  # Known examples.
        #     with self.subTest(a=a, b=b):  # Identify the failing pair if an assertion fails.
        #         self.assertAlmostEqual(multiply(a, b), expected)  # Compare numerical results.

    def test_divide(self):  # Check one ordinary division.
        self.assertEqual(divide(12, 3), 4)  # Check an exact quotient.
        # self.assertAlmostEqual(divide(1, 3), 1 / 3)  # Allow floating-point rounding.
        # self.assertEqual(divide(-9, 3), -3)  # Check a negative numerator.
        # self.assertEqual(divide(0, 3), 0)  # Zero is a valid numerator.

    # def test_divide_by_zero(self):  # Uncomment this test BEFORE restoring the backend guard.
    #     with self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
    #         divide(5, 0)  # This call must raise the expected error and message.

    def test_power(self):
        self.assertEqual(power(2, 3), 8)  # Positive exponent.
        self.assertEqual(power(-2, 3), -8)  # Negative base with an odd exponent.
        self.assertEqual(power(5, 0), 1)  # Zero exponent.
        self.assertEqual(power(2, -2), 0.25)  # Negative exponent gives a reciprocal.
        self.assertEqual(power(0, 4), 0)  # Zero base with a positive exponent.
        self.assertEqual(power(0, 0), 1)  # The convention selected for this lesson.
    #
    # def test_power_zero_negative(self):
    #     with self.assertRaisesRegex(
    #             ValueError, "Zero cannot have a negative exponent"
    #     ):
    #         power(0, -1)

if __name__ == "__main__":  # Run tests only when this file is executed directly.
    unittest.main()  # Collect tests, print results, and exit with a failure code if needed.
