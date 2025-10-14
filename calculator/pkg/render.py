# python
import json


def format_json_output(expression: str, result: float, indent: int = 2) -> str:
    # Normalize float results like 5.0 -> 5 for cleaner output
    if isinstance(result, float) and result.is_integer():
        result_to_dump = int(result)
    else:
        result_to_dump = result

    # Construct a simple, predictable JSON payload
    output_data = {
        "expression": expression,
        "result": result_to_dump,
    }
    # Pretty-print with configurable indentation (default 2 spaces)
    return json.dumps(output_data, indent=indent)