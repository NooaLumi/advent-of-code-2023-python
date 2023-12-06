import sys
import re
from functools import reduce


"""
Advent of Code - Day 4 Part 2

Get the input from https://adventofcode.com/2023/day/4/input, save it to a file and feed it to stdin
ex. `python 04_part2.py < day_four_input.txt` 
"""

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


def get_win_count(nums: list, winning_nums: list):
    return sum(1 for num in nums if num in winning_nums)


def main() -> int:
    data = get_test_data()

    card_number_pattern = re.compile(r'Card\s*(\d+)')
    winning_side_pattern = re.compile(r':(.*?)\|')
    number_side_pattern = re.compile(r'\|(.*?)$')
    number_pattern = re.compile(r'\d+')

    # map of card number to list of card numbers it wins
    card_data = {}

    # generate the map
    for row in data:
        card_number = int(card_number_pattern.findall(row)[0])
        winning_numbers = number_pattern.findall(winning_side_pattern.findall(row)[0])
        numbers = number_pattern.findall(number_side_pattern.findall(row)[0])

        wins = get_win_count(numbers, winning_numbers)
        card_data[card_number] = [card_number + num for num in range(1, wins + 1)]


    def get_winning_cards(cardnum: int):
        """Recursively get number of cards won"""
        winnings = card_data[cardnum]
        return 1 + sum(get_winning_cards(cardnum) for cardnum in winnings) if len(winnings) > 0 else 1


    result =  sum(get_winning_cards(cardnum) for cardnum in card_data)
    print(result)


if __name__ == "__main__":
    sys.exit(main())