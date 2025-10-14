# python
import os

def get_files_info(working_directory, directory="."):
    # Resolve absolute paths for the working directory and the target directory
    abs_work = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, directory))

    # Enforce sandbox: target must be the work dir or a child of it
    inside = abs_target == abs_work or abs_target.startswith(abs_work + os.sep)
    if not inside:
        return f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Validate the target path is a directory before listing
    if not os.path.isdir(abs_target):
        return f'    Error: "{directory}" is not a directory'
    
    try:
        # List directory entries deterministically (sorted)
        listing = sorted(os.listdir(abs_target))
        lines = []
        for name in listing:
            full_path = os.path.join(abs_target, name)
            try:
                # Gather metadata for each entry
                size = os.path.getsize(full_path)
                is_dir = os.path.isdir(full_path)
                # Append a formatted line for this entry
                lines.append(f' - {name}: file_size={size} bytes, is_dir={is_dir}')
            except Exception as e:
                # Return a single error string if any per-entry operation fails
                return f'    Error: {e}'
        # Join all lines into the final string result
        return '\n'.join(lines)
    except Exception as e:
        # Return a single error string if listing the directory fails
        return f'    Error: {e}'
    