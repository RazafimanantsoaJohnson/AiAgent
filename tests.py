from functions.get_files_info import get_files_info

def test_get_files_info():
    test_cases = [["current directory","."], ["'pkg'","pkg"], ["'/bin'","/bin"], ["../","../"]]
    for case in test_cases:
        print(f"Result for {case[0]} directory:")
        print(get_files_info("calculator", case[1]))

if __name__ == "__main__":
    test_get_files_info()

