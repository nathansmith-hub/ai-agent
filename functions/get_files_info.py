# python
import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    # Compute absolute paths for the sandbox root and target
    abs_work = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, directory))

    # Enforce sandbox: target must be the work dir or a subpath
    inside = abs_target == abs_work or abs_target.startswith(abs_work + os.sep)
    if not inside:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Ensure target exists and is a directory
    if not os.path.isdir(abs_target):
        return f'Error: "{directory}" is not a directory'
    
    try:
        # Get deterministic listing
        listing = sorted(os.listdir(abs_target))
        lines = []
        for name in listing:
            full_path = os.path.join(abs_target, name)
            try:
                # Collect basic metadata for each entry
                size = os.path.getsize(full_path)
                is_dir = os.path.isdir(full_path)
                # Format a single-line summary for the entry
                lines.append(f' - {name}: file_size={size} bytes, is_dir={is_dir}')
            except Exception as e:
                # Surface a per-entry error as a single error string
                return f'Error: {e}'
        # Return the aggregated listing
        return '\n'.join(lines)
    except Exception as e:
        # Surface a top-level directory listing error
        return f'Error: {e}'
    
# Function declaration schema for tool usage by the LLM
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
