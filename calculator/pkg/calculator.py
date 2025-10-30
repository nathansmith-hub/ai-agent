# python
class Calculator:
    def __init__(self):
        # Supported binary operators mapped to their implementations
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        # Operator precedence (higher number = higher priority)
        # Note: follow standard arithmetic precedence (* and / bind tighter than + and -)
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        # Treat empty/whitespace-only input as no-op
        if not expression or expression.isspace():
            return None
        # Tokenize by spaces (expects space-separated infix input)
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        # Value stack and operator stack for shunting-yard-like eval
        values = []
        operators = []

        for token in tokens:
            if token in self.operators:
                # Resolve previous operators with higher or equal precedence
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                # Push current operator
                operators.append(token)
            else:
                try:
                    # Parse numeric literal as float (supports ints and decimals)
                    values.append(float(token))
                except ValueError:
                    # Reject unknown tokens early
                    raise ValueError(f"invalid token: {token}")

        # Apply remaining operators
        while operators:
            self._apply_operator(operators, values)

        # A valid expression should collapse to exactly one value
        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        # No-op if no operators (defensive guard)
        if not operators:
            return

        operator = operators.pop()
        # Need two operands for a binary operator
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        # Pop in reverse order: second operand, then first
        b = values.pop()
        a = values.pop()
        # Compute and push the result
        values.append(self.operators[operator](a, b))