import sys
import re
from functools import reduce


"""
Advent of Code - Day 4: Scratchcards

Get the input from https://adventofcode.com/2023/day/4/input, save it to a file and feed it to stdin
ex. `python 04_part1.py < day_four_input.txt` 
"""

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


def get_win_count(nums: list, winning_nums: list):
    return sum(1 for num in nums if num in winning_nums)


def get_score(wins: int):
    return wins if wins < 3 else 2 ** (wins - 1)


def main() -> int:
    data = get_test_data()

    winning_side_pattern = re.compile(r':(.*?)\|')
    number_side_pattern = re.compile(r'\|(.*?)$')
    number_pattern = re.compile(r'\d+')

    scores = []

    for row in data:
        winning_numbers = number_pattern.findall(winning_side_pattern.findall(row)[0])
        numbers = number_pattern.findall(number_side_pattern.findall(row)[0])

        scores.append(get_score(get_win_count(numbers, winning_numbers)))

    
    result = reduce(lambda x, y: x + y, scores, 0)
    print(result)


if __name__ == "__main__":
    sys.exit(main())