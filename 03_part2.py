import sys
import re
from functools import reduce, partial


"""
Advent of Code - Day 3: Gear Ratios

Get the input from https://adventofcode.com/2023/day/3/input, save it to a file and feed it to stdin
ex. `python 03_part2.py < day_three_input.txt` 
"""

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


def main() -> int:
    data = get_test_data()
    last_row_index = len(data) - 1

    number_pattern = re.compile(r'\d+')
    possible_gear_pattern = re.compile(r'[*]')

    is_adjacent = lambda pos1, pos2_start, pos2_end: True if abs(pos1 - pos2_start) == 1 or abs(pos1 - pos2_end) == 1 else False
    is_adjacent_or_overlaps = lambda pos1, pos2_start, pos2_end: True if pos1 >= pos2_start - 1 and pos1 <= pos2_end + 1 else False

    # [[(xpos, value), ...], ...]
    number_rows = [[(match.start(), match.group()) for match in number_pattern.finditer(row)] for row in data]

    gear_ratios = []

    for index, row in enumerate(data):
        # [[xpos, ...], ...]
        possible_gears_in_row = [match.start() for match in possible_gear_pattern.finditer(row)]

        for gear_pos in possible_gears_in_row:
            connected_numbers = []

            get_end_pos = lambda pos, value: pos + (len(value) - 1)
            is_adjacent_to_gear = partial(is_adjacent, gear_pos)
            is_adjacent_to_or_overlaps_gear = partial(is_adjacent_or_overlaps, gear_pos)

            # check if adjacent to numbers on own row
            for num_pos, num_value in number_rows[index]:
                if is_adjacent_to_gear(num_pos, get_end_pos(num_pos, num_value)):
                    connected_numbers.append(num_value)

            # check if adjacent to numbers on previous row
            if index != 0:
                for num_pos, num_value in number_rows[index - 1]:
                    if is_adjacent_to_or_overlaps_gear(num_pos, get_end_pos(num_pos, num_value)):
                        connected_numbers.append(num_value)

            # check if adjacent to numbers on next row
            if index != last_row_index:
                for num_pos, num_value in number_rows[index + 1]:
                    if is_adjacent_to_or_overlaps_gear(num_pos, get_end_pos(num_pos, num_value)):
                        connected_numbers.append(num_value)

            # if adjacent to exactly two numbers, add product of numbers to gear ratios
            if len(connected_numbers) == 2:
                gear_ratios.append(int(connected_numbers[0]) * int(connected_numbers[1]))


    result = reduce(lambda x, y: x + y, gear_ratios, 0)
    print(result)


if __name__ == "__main__":
    sys.exit(main())
