# python
import os

def write_file(working_directory, file_path, content):
    # Resolve the working directory to an absolute, normalized path
    abs_work = os.path.realpath(working_directory).rstrip(os.sep)
    # Resolve the target file path relative to the working directory
    abs_file = os.path.realpath(os.path.join(abs_work, file_path))

    # Sandbox enforcement: allow the working dir itself or any path inside it
    if not (abs_file == abs_work or abs_file.startswith(abs_work + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        # Ensure parent directories exist (noop if they already do)
        os.makedirs(os.path.dirname(abs_file), exist_ok=True)
        # Overwrite or create the file and write the provided content
        with open(abs_file, "w") as f:
            f.write(content)
    except Exception as e:
        # Surface any filesystem error in the required format
        return f'Error: {e}'

    # Confirm success with the required message and character count
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
