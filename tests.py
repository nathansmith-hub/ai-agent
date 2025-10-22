# python
from functions.run_python_file import run_python_file

def test():
    # Case 1: run file calculator/main.py
    result = run_python_file("calculator", "main.py")
    print("Result for main.py:")
    print(result)

    # Case 2: run file calculator/main.py with arguments
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Result for main.py, 3 + 5:")
    print(result)

    # Case 3: write "this should not be allowed" to /tmp/temp.txt
    result = run_python_file("calculator", "tests.py")
    print("Result for tests.py:")
    print(result)

    # Case 4: run file ../main.py
    result = run_python_file("calculator", "../main.py")
    print("Result for ../main.py:")
    print(result)

    # Case 5: run file nonexistent.py
    result = run_python_file("calculator", "nonexistent.py")
    print("Result for nonexistent.py:")
    print(result)

    # Case 6: run file lorem.txt
    result = run_python_file("calculator", "lorem.txt")
    print("Result for lorem.txt:")
    print(result)


if __name__ == "__main__":
    # Run manual tests when executed directly
    test()