# python
import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    # Normalize and resolve absolute paths for sandboxing
    abs_work = os.path.realpath(working_directory).rstrip(os.sep)
    abs_file = os.path.realpath(os.path.join(working_directory, file_path))

    # Enforce sandbox: target file must reside within the working directory
    inside = abs_file.startswith(abs_work + os.sep)
    if not inside:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Ensure the target exists and is a regular file
    if not os.path.isfile(abs_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        # Read up to MAX_CHARS + 1 to detect if truncation is required
        with open(abs_file, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)

        # Truncate and append a notice if content exceeds the limit
        if len(file_content_string) > MAX_CHARS:
            file_content_string = (
                file_content_string[:MAX_CHARS]
                + f'[...File "{file_path}" truncated at 10000 characters]'
            )
        return file_content_string
    except Exception as e:
        # Convert any I/O or OS errors into a standardized error string
        return f"Error: {e}"

# Function declaration schema for tool usage by the LLM
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to read content from, relative to the working directory",
            ),
        },
    ),
)