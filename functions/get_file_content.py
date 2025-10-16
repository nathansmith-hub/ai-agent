# python
import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    # Resolve absolute paths for the working directory and the file path
    abs_work = os.path.realpath(working_directory).rstrip(os.sep)
    abs_file = os.path.realpath(os.path.join(working_directory, file_path))

    # Enforce sandbox: file path must be inside work dir
    inside = abs_file.startswith(abs_work + os.sep)
    if not inside:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Validate the file path is a file before returning
    if not os.path.isfile(abs_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
        if len(file_content_string) > MAX_CHARS:
            file_content_string = file_content_string[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"