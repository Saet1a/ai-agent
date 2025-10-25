import os 
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_work = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_target.startswith(abs_work):
        return f'    Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_target):
        return f'    Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_target, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
            if len(file_content_string) <= MAX_CHARS:
                return file_content_string
            else:
                return file_content_string[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f"Error: {e}"