# python
from functions.write_file import write_file

def test():
    # Case 1: write "wait, this isn't lorem ipsum" to calculator/lorem.txt
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print("Result for lorem.txt:")
    print(result)

    # Case 2: write "lorem ipsum dolor sit amet" to /calculator/pkg/morelorem.txt
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print("Result for pkg/morelorem.txt:")
    print(result)

    # Case 13: write "this should not be allowed" to /tmp/temp.txt
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print("Result for /tmp/temp.txt:")
    print(result)


if __name__ == "__main__":
    # Run manual tests when executed directly
    test()