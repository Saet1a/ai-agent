import os 
from config import MAX_CHARS
from google.genai import types

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
    


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file within the working directory, up to a maximum character limit.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
