import sys
import re
from functools import reduce


"""
Advent of Code - Day 3: Gear Ratios

Get the input from https://adventofcode.com/2023/day/3/input, save it to a file and feed it to stdin
ex. `python 03_part1.py < day_three_input.txt` 
"""

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


def main() -> int:
    data = get_test_data()
    last_row_index = len(data) - 1

    number_pattern = re.compile(r'\d+')
    special_char_pattern = re.compile(r'[^a-zA-Z0-9\s.]')

    is_adjacent = lambda pos1, pos2_start, pos2_end: True if abs(pos1 - pos2_start) == 1 or abs(pos1 - pos2_end) == 1 else False
    is_adjacent_or_overlaps = lambda pos1, pos2_start, pos2_end: True if pos1 >= pos2_start - 1 and pos1 <= pos2_end + 1 else False

    # [[xpos, ...], ...]
    special_char_rows = [[match.start() for match in special_char_pattern.finditer(row)] for row in data]

    part_numbers = []

    for index, row in enumerate(data):
        # [(xpos, value), ...]
        nums_in_row = [(match.start(), match.group()) for match in number_pattern.finditer(row)]

        for num in nums_in_row:
            num_start_pos = num[0]
            num_value = num[1]
            num_end_pos = num_start_pos + (len(num_value) - 1)

            # check if adjacent characters in current, previous or next row
            if  any(is_adjacent(char_pos, num_start_pos, num_end_pos) for char_pos in special_char_rows[index]) or \
                (index != 0 and any(is_adjacent_or_overlaps(char_pos, num_start_pos, num_end_pos) for char_pos in special_char_rows[index - 1])) or \
                (index != last_row_index and any(is_adjacent_or_overlaps(char_pos, num_start_pos, num_end_pos) for char_pos in special_char_rows[index + 1])):
                    part_numbers.append(int(num_value))
                    continue


    result = reduce(lambda x, y: x + y, part_numbers, 0)
    print(result)


if __name__ == "__main__":
    sys.exit(main())
