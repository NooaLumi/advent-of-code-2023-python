import sys
import re
from functools import reduce


"""
Advent of Code - Day 2 Part 2

Get the input from https://adventofcode.com/2023/day/2/input, save it to a file and feed it to stdin
ex. `python 02_part2.py < day_two_input.txt` 
"""

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


def get_minimum_required_power_of_cubes(cube_sets: list) -> bool:
    """Get minimum power of cubes required to make given sets possible"""

    # highest number of each color of cube revealed in a single set
    highest_tallies = {
        'red': 0,
        'green': 0,
        'blue': 0
    }

    for cube_set in cube_sets:
        if highest_tallies[cube_set[2]] < int(cube_set[1]):
            highest_tallies[cube_set[2]] = int(cube_set[1])

    return reduce(lambda x, y: x * y, [value for value in highest_tallies.values()], 1)


def get_sum_of_powers(games_data: list) -> list:
    sets_pattern = re.compile(r'([:,;]) (\d+) (\w+)') # (separator, number, color)
    get_sets = lambda game: sets_pattern.findall(game)

    return reduce(lambda x, y: x + y, [get_minimum_required_power_of_cubes(get_sets(game)) for game in games_data], 0)
        

def main() -> int:
    data = get_test_data()
    result = get_sum_of_powers(data)

    print(result)


if __name__ == "__main__":
    sys.exit(main())