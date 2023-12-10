import sys
import re


"""
Advent of Code - [DAY_NAME]

Get the input from [INPUT_URL], save it to a file and feed it to stdin
ex. `python [SCRIPT_NAME].py < [TEXT_FILE_NAME].txt` 
"""

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


def main() -> int:
    data = get_test_data()


if __name__ == "__main__":
    sys.exit(main())