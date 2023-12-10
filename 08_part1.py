import sys
import re
from functools import reduce


"""
Advent of Code - Day 8: Haunted Wasteland

Get the input from https://adventofcode.com/2023/day/8/input, save it to a file and feed it to stdin
ex. `python 08_part1.py < day_eight_input.txt` 
"""

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


def find_nodes_in_row(row: str) -> tuple:
    return re.findall(r'^(.*?)(?:\s=\s\()(.*?)(?:,\s)(.*?)(?:\))', row)[0]


def network_data_reducer(network: dict, row: str) -> dict:
    nodes = find_nodes_in_row(row)
    return {**network, nodes[0]: (nodes[1], nodes[2])}


def main() -> int:
    data = get_test_data()

    # directions in a list where 0 = left, 1 = right
    directions = list(map(lambda x: 0 if x == 'L' else 1, re.findall(r'.', data[0])))

    # network in a dict {node: (left_node, right_node), ...n}
    network = reduce(network_data_reducer, data[2:], {})

    # keep track of current node and step count
    current_node = 'AAA'
    step_count = 0 

    while current_node != 'ZZZ':
        # cyclically index directions
        direction = directions[step_count % len(directions)]
        step_count += 1

        current_node = network[current_node][direction]

    result = step_count
    print(result)


if __name__ == "__main__":
    sys.exit(main())