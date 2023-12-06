import sys
import re
from functools import reduce


"""
Advent of Code - Day 1 Part 2

Get the input from https://adventofcode.com/2023/day/1/input, save it to a file and feed it to stdin
ex. `python 01_part2.py < day_one_input.txt` 
"""

"""Map of english words for digits to numeric digits"""
WORDS_TO_DIGITS_MAP = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

"""Shortest word in WORDS_TO_DIGITS_MAP"""
SHORTEST_WORD_LENGTH = min(len(w) for w in WORDS_TO_DIGITS_MAP.keys())


def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


def get_first_digit_in_string(input: str) -> (str | None, int | None):
    """Get index and value of the first numeric digit that appears in given string"""

    for index, char in enumerate(input):
        if char.isnumeric(): return char, index
    return None, None


def get_last_digit_in_string(input: str) -> (str | None, int | None):
    """Get index and value of the last numeric digit that appears in given string"""

    digit, index = get_first_digit_in_string(reversed(input))
    return digit, (len(input) - 1 - index if index != None else None)


def get_word_instances_in_string(word: str, input: str) -> list:
    """find indeces of occurrences of word in string"""
    return [match.start() for match in re.finditer(word, input)]


sum_numbers = lambda x, y: x + y

def extract_calibration_value_from_string(input: str) -> int:
    """Extract first and last digit (numeric or worded) from given string"""

    input_length = len(input)

    # search for numeric digits
    first_digit, first_digit_index = get_first_digit_in_string(input)
    last_digit, last_digit_index = get_last_digit_in_string(input)

    # if we already found the first and last digit, return them
    if first_digit != None and (first_digit_index + 1 < SHORTEST_WORD_LENGTH) and (last_digit_index + 1 > input_length - SHORTEST_WORD_LENGTH): return int(first_digit + last_digit)

    # search for word digits
    for word in WORDS_TO_DIGITS_MAP:
        # if word is longer than input string, skip word
        if len(word) > input_length: continue

        # find indeces of occurrences of word in string
        matches = get_word_instances_in_string(word, input)

        # if no matches, continue
        if len(matches) == 0: continue

        # get first and last occurrence of word in input string
        first_occurrence = min(matches)
        last_occurrence = max(matches)

        # if first so far, assign
        if first_digit == None or first_occurrence < first_digit_index:
            first_digit = WORDS_TO_DIGITS_MAP[word]
            first_digit_index = first_occurrence
            
        # if last so far, assign
        if last_digit == None or last_occurrence > last_digit_index:
            last_digit = WORDS_TO_DIGITS_MAP[word]
            last_digit_index = last_occurrence

    return int(first_digit + last_digit) if first_digit != None else 0


def main() -> int:
    data = get_test_data()

    # extract calibration value from each item in data, and sum all of them together
    result = reduce(sum_numbers, [extract_calibration_value_from_string(line) for line in data], 0)

    print(result)

if __name__ == "__main__":
    sys.exit(main())