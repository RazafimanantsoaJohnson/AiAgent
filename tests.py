from functions.get_files_info import get_files_info, get_file_content
from functions.write_file import write_file
from functions.run_code import run_python_file

import subprocess

def test_get_files_info():
    test_cases = [["current directory","."], ["'pkg'","pkg"], ["'/bin'","/bin"], ["../","../"]]
    for case in test_cases:
        print(f"Result for {case[0]} directory:")
        print(get_files_info("calculator", case[1]))

def test_get_files_content():
    test_cases = ["main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]
    for case in test_cases:
        print(f"Result for {case} file: ")
        print(get_file_content("calculator",case))

def test_write_file():
    test_cases = [
        ["calculator","lorem.txt", "wait, this isn't lorem ipsum"],
        ["calculator","pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
        ["calculator","/tmp/temp.txt", "this should not be allowed"]
    ]
    for case in test_cases:
        print(f"Result for {case[1]}")
        print(write_file(case[0],case[1],case[2]))

def test_run_python_file():
    test_cases = [
        ["calculator", "main.py"],
        ["calculator", "../main.py"],
        ["calculator", "main.py", ["2 + 5"]],
        ["calculator","tests.py"],
        ["calculator","nonexistent.py"],
        ["calculator","lorem.txt"]
    ]
    i= 0
    for case in test_cases:
        print("===Execution {i}:")
        i+= 1
        if len(case)>2:
            print(run_python_file(case[0],case[1],case[2]))
            continue
        print(run_python_file(case[0], case[1]))

if __name__ == "__main__":
    # test_get_files_info()
    # test_get_files_content()
    # test_write_file()
    # result = subprocess.run(["ls"], timeout=50, capture_output = True, text=True)
    # print(result)
    test_run_python_file()

