# python
from google.genai import types

# Import available tool functions the model may call
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    # Extract the chosen function's name and its argument dict from the model
    function_name = function_call_part.name
    args = function_call_part.args

    # Verbose: show name and full args; otherwise, just the name
    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    # Map of function names (strings) to actual callables
    functions_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    # Start from provided args (or empty), then inject the required working directory
    call_args = dict(args) if args is not None else {}
    call_args.setdefault("working_directory", "./calculator")

    # Look up the target function by name
    func = functions_map.get(function_name)
    if func is None:
        # Return a tool response indicating the function name was invalid
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Execute the function with keyword arguments and capture the result
    result = func(**call_args)

    # Return a standardized tool response wrapping the result
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )
