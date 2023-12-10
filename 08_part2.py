import sys
import re
from functools import reduce


"""
Advent of Code - Day 8 Part 2

Get the input from https://adventofcode.com/2023/day/8/input, save it to a file and feed it to stdin
ex. `python 08_part2.py < day_eight_input.txt` 
"""

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


def find_nodes_in_row(row: str) -> tuple:
    return re.findall(r'^(.*?)(?:\s=\s\()(.*?)(?:,\s)(.*?)(?:\))', row)[0]


def network_data_reducer(network: dict, row: str) -> dict:
    nodes = find_nodes_in_row(row)
    return {**network, nodes[0]: (nodes[1], nodes[2])}


def get_gcd(x, y):
    """Get the greatest common divisor using the euclidean algorithm https://en.wikipedia.org/wiki/Euclidean_algorithm"""
    return x if y == 0 else get_gcd(y, x % y)


def get_lcm(x, y):
    """get least common multiple using the gcd https://en.wikipedia.org/wiki/Least_common_multiple"""
    return x * (y / get_gcd(x, y))


def main() -> int:
    data = get_test_data()

    # directions in a list where 0 = left, 1 = right
    directions = list(map(lambda x: 0 if x == 'L' else 1, re.findall(r'.', data[0])))

    # network in a dict {node: (left_node, right_node), ...n}
    network = reduce(network_data_reducer, data[2:], {})

    # get starting nodes (ones that end in 'A')
    starting_nodes = {node: [dest_nodes[0], dest_nodes[1], 0] for node, dest_nodes in network.items() if node[2] == 'A'}

    # calculate "step cycle" in which node meets a '**Z' node
    for node in starting_nodes:
        current_node = node
        step_count = 0

        while current_node[2] != 'Z':
            # cyclically index directions
            direction = directions[step_count % len(directions)]
            step_count += 1

            current_node = network[current_node][direction]

        # add cycle length to the starting nodes dictionary
        starting_nodes[node][2] = step_count


    # get least common multiple of all step cycles (eg. the smallest step count where they all meet)
    step_cycles = [node[2] for node in starting_nodes.values()]
    result = step_cycles[0]
    for node in step_cycles[1:]:
        result = get_lcm(node, result)

    print(round(result))

    # again, brute force did not work :P
    # while not all(node[2] == 'Z' for node in current_nodes.keys()):
    #     # cyclically index directions
    #     direction = directions[step_count % len(directions)]
    #     step_count += 1

    #     current_nodes = {dest_nodes[direction]: network[dest_nodes[direction]] for dest_nodes in current_nodes.values()}

    # this one was also too heavy to compute
    # nodes = [node[2] for node in starting_nodes.values()]
    # largest_cycle = max(nodes)
    # loop = 1
    # while not all((largest_cycle * loop) % node == 0 for node in nodes):
    #     loop += 1


if __name__ == "__main__":
    sys.exit(main())