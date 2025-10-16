# python
from functions.get_file_content import get_file_content

def test():
    # Case 1: list contents of calculator", "main.py")
    result = get_file_content("calculator", "main.py")
    print("Result for main.py:")
    print(result)

    # Case 2: list contents of pkg/calculator.py
    result = get_file_content("calculator", "pkg/calculator.py")
    print("Result for pkg/calculator.py:")
    print(result)

    # Case 1: list contents of /bin/cat
    result = get_file_content("calculator", "/bin/cat")
    print("Result for /bin/cat:")
    print(result)

    # Case 1: list contents of pkg/does_not_exist.py
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print("Result for pkg/does_not_exist.py:")
    print(result)


if __name__ == "__main__":
    # Run manual tests when executed directly
    test()