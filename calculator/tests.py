# python
import unittest
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        # Fresh calculator instance for each test to avoid shared state
        self.calculator = Calculator()

    def test_addition(self):
        # Basic addition
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        # Basic subtraction
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        # Basic multiplication
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        # Basic division
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        # Operator precedence: multiplication before addition
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        # Mixed operators with correct precedence handling
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        # Empty input should return None (handled gracefully)
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        # Unknown operator should raise a ValueError
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        # Insufficient operands for an operator should raise ValueError
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")


if __name__ == "__main__":
    # Allow running tests directly via `python tests.py`
    unittest.main()