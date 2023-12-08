import sys
import re


"""
Advent of Code - Day 6: Wait For It

Get the input from https://adventofcode.com/2023/day/6/input, save it to a file and feed it to stdin
ex. `python 06_part2.py < day_six_input.txt` 
"""

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


def get_distance_for_input(btn_hold_time: int, race_time: int):
    time_to_travel = race_time - btn_hold_time

    # distance = time to travel * acceleration (button hold time)
    return time_to_travel * btn_hold_time


get_number_from_row = lambda row: int(''.join(re.findall(r'\d+', row)))


def main() -> int:
    data = get_test_data()

    race_time = get_number_from_row(data[0])
    distance_to_beat = get_number_from_row(data[1])

    ways_to_beat = 0

    for btn_hold_time in range(0, race_time + 1):
        if get_distance_for_input(btn_hold_time, race_time) > distance_to_beat:
            ways_to_beat += 1

    print(ways_to_beat)


if __name__ == "__main__":
    sys.exit(main())