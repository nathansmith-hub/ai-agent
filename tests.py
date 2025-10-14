# python
from functions.get_files_info import get_files_info

def test():
    # Case 1: list contents of the working directory itself
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)

    # Case 2: list a subdirectory inside the working directory
    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)

    # Case 3: attempt to access an absolute path outside the sandbox
    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)

    # Case 4: attempt to escape the sandbox with a relative path
    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(result)


if __name__ == "__main__":
    # Run manual tests when executed directly
    test()