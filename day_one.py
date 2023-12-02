import sys
from functools import reduce


"""
Advent of Code - Day 1: Trebuchet?!

Get the input from https://adventofcode.com/2023/day/1/input, save it to a file and feed it to stdin
ex. `python day_one.py < day_one_input.txt` 
"""

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


get_first_digit_in_string = lambda x: next(d for d in x if d.isnumeric())
get_last_digit_in_string = lambda x: get_first_digit_in_string(reversed(x))
sum_numbers = lambda x, y: x + y


def extract_calibration_value_from_string(input: str) -> int:
    """Extract first and last digit from given string"""
    try:
        digits = get_first_digit_in_string(input) + get_last_digit_in_string(input)
        return int(digits)
    except StopIteration:
        # no digits in given input string
        return 0


def main() -> int:
    data = get_test_data()

    # extract calibration value from each item in data, and sum all of them together
    result = reduce(sum_numbers, [extract_calibration_value_from_string(line) for line in data], 0)

    print(result)

if __name__ == "__main__":
    sys.exit(main())