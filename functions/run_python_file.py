# python
import os
import sys
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    # Resolve absolute paths to avoid path traversal and normalize inputs
    abs_work = os.path.realpath(working_directory).rstrip(os.sep)
    abs_file = os.path.realpath(os.path.join(working_directory, file_path))

    # Sandbox: require target to be inside working_directory
    inside = abs_file.startswith(abs_work + os.sep)
    if not inside:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Validate file exists and is a regular file
    if not os.path.isfile(abs_file):
        return f'Error: File "{file_path}" not found.'
    
    # Validate Python file extension
    _, ext = os.path.splitext(file_path)
    if ext.lower() != '.py':
        return f'Error: "{file_path}" is not a Python file.'
    
    # Execute the Python file and capture results
    try:
        # Ensure args is a sequence of strings
        args = list(map(str, args))
        # Use the current interpreter for portability
        command = [sys.executable, abs_file] + args

        completed_process = subprocess.run(
            command,
            cwd=abs_work,           # Set working directory for relative paths/imports
            timeout=30,             # Prevent long-running processes
            capture_output=True,    # Capture both stdout and stderr
            text=True               # Decode output as text (str) instead of bytes
        )

        # Normalize outputs for consistent formatting
        stripped_stdout = completed_process.stdout.strip()
        stripped_stderr = completed_process.stderr.strip()

        # If neither stream produced output, report explicitly
        if stripped_stdout == "" and stripped_stderr == "":
            return "No output produced."

        # Build the formatted output
        output = f"STDOUT: {stripped_stdout}\nSTDERR: {stripped_stderr}"

        # Include non-zero exit code information if applicable
        if completed_process.returncode != 0:
            output += f"\nProcess exited with code {completed_process.returncode}"

        return output
    except Exception as e:
        # Catch unexpected execution errors and return a standardized message
        return f"Error: executing Python file: {e}"

