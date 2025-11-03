from functions.run_python_file import run_python_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

def test():
    result = get_file_content({'file_path': 'main.py'})
    print(result)

    result = write_file({'file_path': 'main.txt', 'content': 'hello'})
    print(result)

    result = get_files_info({'directory': 'pkg'})
    print(result)

    result = run_python_file({'file_path': 'main.py'})      
    print(result)




if __name__ == "__main__":
    test()