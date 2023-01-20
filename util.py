from common import *


def print_grid(map: Map):
    for line in map.grid:
        print(line)


def get_map(level: int):
    with open("levels.txt", mode="r") as file:
        lines = file.readlines()
        return Map(lines[level-1])
