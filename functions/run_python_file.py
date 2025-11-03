import os, subprocess
from config import MAX_CHARS
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_work = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_target.startswith(abs_work):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_target):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: File "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python", abs_target] + args,   
            capture_output=True,             
            text=True,                      
            cwd=abs_work,                    
            timeout=30                       
        )

        
        output = []
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")

        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the working directory and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A list of arguments to pass to the Python script.",
                ),
                description="A list of arguments to pass to the Python script.",
            ),
        },
        required=["file_path"],
    ),
)