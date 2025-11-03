from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
FUNCTIONS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

def call_function(function_call_part, verbose=False):
    name = function_call_part.name
    args = function_call_part.args
    kwargs = dict(args or {})      
    kwargs["working_directory"] = "./calculator"
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    print(f" - Calling function: {function_call_part.name}")

    fn = FUNCTIONS.get(function_call_part.name)
    if fn is None:
        return types.Content(role="tool",parts=[types.Part.from_function_response(name=function_call_part.name,response={"error": f"Unknown function: {function_call_part.name}"},)],)
    
    result = fn(**kwargs)
    return types.Content(role="tool",parts=[types.Part.from_function_response(name=function_call_part.name,response={"result": result},)],)




