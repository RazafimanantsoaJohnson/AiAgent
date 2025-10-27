from functions.get_files_info import get_files_info, get_file_content

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

if __name__ == "__main__":
    test_get_files_info()
    test_get_files_content()

