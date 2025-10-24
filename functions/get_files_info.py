import os

def get_files_info(working_directory, directory="."):
    abs_work = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, directory))
    if not abs_target.startswith(abs_work):
        return f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_target):
        return f'    Error: "{directory}" is not a directory'
    try:
        files_info = []
        for file in os.listdir(abs_target):
            file_path = os.path.join(abs_target,file)
            files_info.append(f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"
