import sys
import re
from functools import reduce


"""
Advent of Code - Day 2: Cube Conundrum 

Get the input from https://adventofcode.com/2023/day/2/input, save it to a file and feed it to stdin
ex. `python day_two.py < day_two_input.txt` 
"""

# Color and number of cubes that can appear at once
CUBES_IN_BAG = {
    'red': 12,
    'green': 13,
    'blue': 14
}

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


def check_is_game_possible(cube_sets: list) -> bool:
    # track cubes revealed in a single set
    set_tally = {
        'red': 0,
        'green': 0,
        'blue': 0
    }

    for cube_set in cube_sets:
        if cube_set[0] == ':' or cube_set[0] == ';':
            # new set, clear tally
            set_tally['red'], set_tally['green'], set_tally['blue'] = 0, 0, 0

        # add to tally
        set_tally[cube_set[2]] = int(cube_set[1])

        # check tally against total cubes
        for color, cube_count in CUBES_IN_BAG.items():
            if set_tally[color] > cube_count: return False
        
    return True


def get_possible_games(games_data: list) -> list:
    """Get list of possible games' numbers"""

    game_number_pattern = re.compile(r'Game (\d+)') # (game_number)
    sets_pattern = re.compile(r'([:,;]) (\d+) (\w+)') # (separator, number, color)

    get_game_number = lambda game: int(game_number_pattern.findall(game)[0])
    get_sets = lambda game: sets_pattern.findall(game)
    filter_none = lambda x: list(filter(lambda x: x is not None, x))

    # return list of possible games' numbers
    return filter_none([
        (get_game_number(game) if check_is_game_possible(get_sets(game)) else None) for game in games_data 
    ])
        

def main() -> int:
    data = get_test_data()
    possible_games = get_possible_games(data)
    result = reduce(lambda x, y: x + y, possible_games, 0)

    print(result)


if __name__ == "__main__":
    sys.exit(main())