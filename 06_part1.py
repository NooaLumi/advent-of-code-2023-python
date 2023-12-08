import sys
import re
from functools import reduce


"""
Advent of Code - Day 6: Wait For It

Get the input from https://adventofcode.com/2023/day/6/input, save it to a file and feed it to stdin
ex. `python 06_part1.py < day_six_input.txt` 
"""

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


def get_distance_for_input(btn_hold_time: int, race_time: int):
    time_to_travel = race_time - btn_hold_time

    # distance = time to travel * acceleration (button hold time)
    return time_to_travel * btn_hold_time


get_numbers_from_row = lambda row: list(map(lambda x: int(x), re.findall(r'\d+', row)))


def main() -> int:
    data = get_test_data()

    race_times = get_numbers_from_row(data[0])
    race_distances = get_numbers_from_row(data[1])

    ways_to_beat_races = []

    for i, race_time in enumerate(race_times):
        distance_to_beat = race_distances[i]
        ways_to_beat = 0

        for btn_hold_time in range(0, race_time + 1):
            distance = get_distance_for_input(btn_hold_time, race_time)
            if distance > distance_to_beat:
                ways_to_beat += 1

        ways_to_beat_races.append(ways_to_beat)

    result = reduce(lambda x, y: x * y, ways_to_beat_races, 1)
    print(result)


if __name__ == "__main__":
    sys.exit(main())