# python
import sys
from pkg.calculator import Calculator
from pkg.render import format_json_output


def main():
    # Instantiate the calculator engine
    calculator = Calculator()

    # If no expression is provided, show usage and exit gracefully
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    # Join all CLI args into a single space-separated expression
    expression = " ".join(sys.argv[1:])
    try:
        # Evaluate the infix expression (e.g., "3 * 4 + 5")
        result = calculator.evaluate(expression)
        if result is not None:
            # Render a consistent JSON string for CLI consumption
            to_print = format_json_output(expression, result)
            print(to_print)
        else:
            # Explicitly handle empty or whitespace-only input
            print("Error: Expression is empty or contains only whitespace.")
    except Exception as e:
        # Catch and report evaluation errors without a stack trace
        print(f"Error: {e}")


if __name__ == "__main__":
    # Standard CLI entrypoint
    main()