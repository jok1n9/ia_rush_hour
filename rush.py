from tree_search import *
from common import *


class RushHour(SearchDomain):

    def __init__(self, map):
        self.pieces = []
        self.keys = []
        for y, line in enumerate(map.grid):
            for x, collumn in enumerate(line):
                char = map.get(Coordinates(x, y))
                if char != map.empty_tile and char != map.wall_tile and char not in self.pieces:
                    self.pieces.append(char)

    def actions(self, map):
        vectors = [Coordinates(1, 0), Coordinates(-1, 0),
                   Coordinates(0, 1), Coordinates(0, -1)]
        actions = []
        for piece in self.pieces:
            for vec in vectors:
                new = Map(str(map))
                try:
                    new.move(piece, vec)
                    actions.append((piece, vec))
                except MapException:
                    pass
        return actions

    def result(self, map, action):
        new = Map(str(map))
        new.move(action[0], action[1])
        return new

    def cost(self, grid, action):
        return 1

    def heuristic(self, map: Map):
        blocking_cars = 0
        a = map.piece_coordinates("A")
        for piece in self.pieces:
            if piece != "A":
                if any(coordinate.y == a[0].y for coordinate in map.piece_coordinates(piece)):
                    blocking_cars += 1
        return blocking_cars

    def heuristic2(self, map: Map):
        blocking_cars = []
        a = map.piece_coordinates("A")
        distance_to_end = map.grid_size-1 - a[-1].x
        heuristic = 0
        for piece in self.pieces:
            if piece != "A":
                if any(coordinate.y == a[0].y for coordinate in map.piece_coordinates(piece)):
                    blocking_cars += [piece]

        for blocking in blocking_cars:
            blocking_x = map.piece_coordinates(blocking)[0].x
            blocking_y = map.piece_coordinates(blocking)[0].y
            over = 0
            under = 0
            for piece in self.pieces:
                if piece not in blocking_cars:
                    # All blocking cars are vertical
                    if self.orientation(piece, map) == "H":
                        # print(piece)
                        if any(coordinate.x == blocking_x for coordinate in map.piece_coordinates(piece)):
                            if map.piece_coordinates(piece)[0].y < blocking_y:
                                over += 1
                            else:
                                under += 1
                        heuristic += len(blocking_cars) + min(over, under)

        return heuristic

    def orientation(self, piece, map: Map):
        p = map.piece_coordinates(piece)
        return "V" if p[0].x == p[1].x else "H"

    def satisfies(self, map):
        return map.test_win()
