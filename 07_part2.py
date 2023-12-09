import sys
from functools import reduce
import re


"""
Advent of Code - Day 7: Camel Cards Part 2

Get the input from https://adventofcode.com/2023/day/7/input, save it to a file and feed it to stdin
ex. `python 07_part2.py < day_seven_input.txt` 
"""

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


# cards ranked in order of strength
CARD_RANKS = [
    'A', 'K', 'Q', 'T', 
    '9', '8', '7', '6', '5', '4', '3', '2', 'J'
]

def get_hand_strength(hand: list) -> int:
    """Get a strength value for the given hand"""

    # get counts of each unique card we have ex. {'J': 2, 'K': 3}
    ranks_to_counts = reduce(lambda combined, c: {**combined, c: (combined.get(c) or 0) + 1}, hand, {})

    # get joker count
    jokers = ranks_to_counts.get('J') or 0

    # get other card counts (no jokers) in order of what we have the most ex. [3, 2], [1, 1, 1, 1, 1]
    card_counts = sorted([count for card, count in ranks_to_counts.items() if card != 'J'], reverse=True)

    # function to get card count with jokers included
    with_jokers = lambda c: c + jokers

    # get hand strength
    strength = (
        7 if jokers == 5 or with_jokers(card_counts[0]) == 5 else                                                                   # five of a kind (5)
        6 if with_jokers(card_counts[0]) == 4 else                                                                                  # four of a kind (4, 1)
        5 if (jokers == 1 and card_counts[1] == 2) or (card_counts[0] == 3 and card_counts[1] == 2) else                            # full house (3, 2)
        4 if with_jokers(card_counts[0]) == 3 else                                                                                  # three of a kind (3,)
        3 if card_counts[0] == 2 and card_counts[1] == 2 else                                                                       # two pairs (2, 2, 1)
        2 if jokers == 1 or card_counts[0] == 2 else                                                                                # two of a kind (2,)
        1 if all(x == 1 for x in card_counts) else                                                                                  # all uniques (1, 1, 1, 1, 1)
        0                                                                                                                           # nothing :(
    )

    # get strengths of individual cards
    individual_card_strengths = ['{:02d}'.format(((len(CARD_RANKS) - 1) - CARD_RANKS.index(card))) for card in hand]

    # return a comprehensive hand strength (type and individual cards) that we can use to compare hands to eachother
    return int(str(strength) + ''.join(individual_card_strengths))


def main() -> int:
    data = get_test_data()

    hands = []

    for row in data:
        hand, bid = re.findall(r'(.*)\s(\d+)', row)[0]

        # get hand strength
        strength = get_hand_strength(list(hand))

        # add tuple to list (strength, bid)
        hands.append((strength, int(bid)))


    winnings = 0
    # loop cards in order of strength (strongest first)
    for index, hand in enumerate(sorted(hands, reverse=True)):
        bid = hand[1]

        # get rank by placement in sorted array (last index = rank 1)
        rank = len(hands) - index

        # add to winnings
        winnings += bid * rank


    print(winnings)


if __name__ == "__main__":
    sys.exit(main())