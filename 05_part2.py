import sys
import re
from typing import Callable

sys.setrecursionlimit(1500)


"""
Advent of Code - Day 5: If You Give A Seed A Fertilizer

Get the input from https://adventofcode.com/2023/day/5/input, save it to a file and feed it to stdin
ex. `python 05_part1.py < day_five_input.txt` 
"""

def get_test_data():
    """Get test data from stdin"""
    return [line.rstrip() for line in sys.stdin]


def generate_maps_from_raw_data(data: list):
    """
    Generate source/destination maps from raw stdin data

    Returns:
        destination / source map [[((dest_range_start, dest_range_end), (source_range_start, source_range_end)), ...n], ...n]

    """

    maps = []
    current_map_index = -1

    # loop rows (skip first row -> seeds)
    for row in data[1:]:
        # empty row, continue
        if len(row) == 0: continue

        # numbers row 
        if row[0].isnumeric():
            dest_range_start, source_range_start, range_length = map(lambda x: int(x), re.findall(r'\d+', row))
            maps[current_map_index].append((
                (dest_range_start, dest_range_start + (range_length - 1)),      # 0: destination range (start, end)
                (source_range_start, source_range_start + (range_length - 1)),  # 1: source range (start, end)
            ))

        # map name row
        else:
            maps.append([])
            current_map_index += 1

    return maps


def get_range_overlap(range1: tuple, range2: tuple) -> tuple:
    """
    Get portion of range1 that matches range2, and portions that don't
    
    Returns:
        (matches[range,...n], leftovers[range,...n])

    """

    # if ranges don't overlap at all, return everything as leftovers
    if range1[0] > range2[1] or range1[1] < range2[0]: return (None, [range1])

    # if range2 encompasses all of range1, return everything as a match
    if range1[0] >= range2[0] and range1[1] <= range2[1]: return (range1, [])

    # if ranges are a perfect match, return everything as a match
    if range1[0] == range2[0] and range1[1] == range2[1]: return (range1, [])

    # range1 starts at or before range2
    if range1[0] <= range2[0]:
        # if range1 ends at or after range2, return entire range2 as match and rest as leftovers (range1 encompasses all of range2)
        if range1[1] >= range2[1]: 
            leftovers = []
            if range1[0] != range2[0]: leftovers.append((range1[0], range2[0] - 1)) # from start of range1 to start of range2
            if range1[1] != range2[1]: leftovers.append((range2[1] + 1, range1[1])) # from end of range2 to end of range1
            return (range2, leftovers)

        # range1 starts before range2, but ends somewhere in the middle of it
        # return matching portion, and leftovers from the beginning of range1
        return ((range2[0], range1[1]), [(range1[0], range2[0] - 1)])

    else:
        # range1 starts after range2 starts and ends after range2 ends, but they intersect somewhere in the middle
        # return matching portion, and leftovers from the end of range1
        return((range1[0], range2[1]), [(range2[1] + 1, range1[1])])


def create_get_destination_ranges_for_source_range(range_maps: list) -> Callable[[tuple], list]:
    """Create function that finds destination ranges for given source range from given range map"""

    def source_to_destination(source_range: tuple) -> list:
        """Translate source range to destination ranges"""
        dest_ranges = []
        total_leftover_ranges = []

        # loop though each range map (destination_range, source_range)
        for index, range_map in enumerate(range_maps):
            dest_map_range = range_map[0]
            source_map_range = range_map[1]

            matching_range, leftover_ranges = get_range_overlap(source_range, source_map_range)

            if matching_range != None:
                # normalize matching range out of source map range, translate to destination range
                dest_ranges.append((
                    matching_range[0] - source_map_range[0] + dest_map_range[0],
                    matching_range[1] - source_map_range[1] + dest_map_range[1],
                ))

            if index == 0:
                # save possible leftover ranges
                total_leftover_ranges.extend(leftover_ranges)
            else:
                # check if leftover ranges can be whittled down by this range map
                for index, leftover_range in enumerate(total_leftover_ranges):
                    matching_range, leftover_ranges = get_range_overlap(leftover_range, source_map_range)
                    if matching_range != None:
                        # delete leftover range, add any possible new (smaller) leftovers
                        del total_leftover_ranges[index]
                        total_leftover_ranges.extend(leftover_ranges)

        return dest_ranges + total_leftover_ranges

    return source_to_destination



def main() -> int:
    data = get_test_data()

    # Brute force did not work lmao, leaving it here so I can laugh at myself later
    # source_numbers = []
    # seeds = list(map(lambda i: int(i), number_pattern.findall(data[0])))
    # for index, seed in enumerate(seeds):
    #     if index % 2 == 0:
    #         for num in range(seed, seed + (seeds[index + 1] - 1)):
    #             source_numbers.append(num)

    # get map data [[(dest_range, source_range), ...n], ...n]
    maps = generate_maps_from_raw_data(data)

    source_ranges = []
    dest_ranges = []

    # get inital source ranges from seeds
    source_ranges = []
    seeds = list(map(lambda i: int(i), re.findall(r'\d+', data[0])))
    for index, seed in enumerate(seeds):
        if seed % 2 == 0:
            source_ranges.append((seed, seed + (seeds[index + 1] - 1)))

    # loop through each each range map (seed-to-soil, soil-to-fertilizer, etc.)
    for index, range_maps in enumerate(maps):
        # create function to convert from source range to destination range(s)
        source_to_destination = create_get_destination_ranges_for_source_range(range_maps)

        # get destination ranges for each source range
        for source_range in source_ranges:
            dest_ranges.extend(source_to_destination(source_range))

        # make discovered destination ranges the new source ranges (unless last map eg. location)
        if index != (len(maps) - 1):
            source_ranges = dest_ranges
            dest_ranges = []

    # get range that starts from smallest number
    result = min(map(lambda x: x[0], dest_ranges))

    print(result)

if __name__ == "__main__":
    sys.exit(main())