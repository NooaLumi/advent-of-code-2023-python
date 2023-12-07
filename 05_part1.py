import sys
import re
from typing import Callable


"""
Advent of Code - Day 5: If You Give A Seed A Fertilizer

Get the input from https://adventofcode.com/2023/day/5/input, save it to a file and feed it to stdin
ex. `python 05_part1.py < day_five_input.txt` 
"""

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


def create_destination_finder(dest_range_start: int, source_range_start: int, range_length: int) -> Callable[[int], int | None]:
    """Create function that translates source numbers to destination numbers"""

    def source_to_destination(source_num: int) -> int | None:
        """Translate source number to a destination number"""
        # if in source range
        if source_num >= source_range_start and source_num <= source_range_start + (range_length - 1):
            # normalize number out of source range, translate to destination range
            return (source_num - source_range_start) + dest_range_start
        else:
            return None

    return source_to_destination
    

def main() -> int:
    data = get_test_data()

    # [0: map_from, 1: map_to]
    map_pattern = re.compile(r'^(.*?)(?:-to-)(.*?)(?:\smap)')

    number_pattern = re.compile(r'\d+')

    # get list of seeds (our initial source numbers)
    source_numbers = list(map(lambda i: int(i), number_pattern.findall(data[0])))
    dest_numbers = []
    matched_sources = []

    # loop rows (skip first row -> seeds)
    for row in data[1:]:
        # empty row, continue
        if len(row) == 0: continue

        # number row
        if row[0].isnumeric():
            # create function for matching source number to destination
            find_dest = create_destination_finder(*map(lambda x: int(x), number_pattern.findall(row)))

            for source_num in source_numbers:
                # find matching destination number
                dest_num = find_dest(source_num)

                # if no match, continue
                if dest_num == None: continue

                # save matched destination- and source numbers
                dest_numbers.append(dest_num)
                matched_sources.append(source_num)

        # map row
        else:
            # add unmatched source numbers to destination numbers
            for source_num in source_numbers:
                if source_num in matched_sources: continue
                dest_numbers.append(source_num)

            # destination numbers are the new source numbers for next map
            source_numbers = dest_numbers
            
            # clear matched and destination numbers
            matched_sources = []
            dest_numbers = []


    result = min(dest_numbers)
    print(result)


if __name__ == "__main__":
    sys.exit(main())