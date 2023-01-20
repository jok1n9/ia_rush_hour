
from common import *


class Cursor():

    def __init__(self, position, map=None):
        self.x = position[0]
        self.y = position[1]
        self.selected = False
        self.keys = []

    def update(self, position, map=None):
        self.x = position.x
        self.y = position.y

        self.map = map

    def select(self):
        """ select cursor """
        self.selected = not self.selected
        self.keys.append(' ')
        return 0

    def force_unselect(self):
        if (self.selected):
            self.select()
        return 0

    def force_select(self):
        if (not self.selected):
            self.select()
        return 0

    def return_cursor(self):
        return Coordinates(self.x, self.y)

    def move(self, goal):
        """ move cursor to position"""
        movex = self.x - goal.x
        movey = self.y - goal.y

        if movex < 0:
            movex = movex*-1
            for i in range(movex):
                self.keys.append('d')
        else:
            for i in range(movex):
                self.keys.append('a')
        if movey < 0:
            movey = movey*-1
            for i in range(movey):
                self.keys.append('s')
        else:
            for i in range(movey):
                self.keys.append('w')

        self.update(goal)
        return 0

    def move_keys(self, goal):
        """ all keys per move(without translation)"""
        movex = self.x - goal.x
        movey = self.y - goal.y
        self.keys = []
        if movex < 0:
            movex = movex*-1
            for i in range(movex):
                self.keys.append('d')
        else:
            for i in range(movex):
                self.keys.append('a')
        if movey < 0:
            movey = movey*-1
            for i in range(movey):
                self.keys.append('s')
        else:
            for i in range(movey):
                self.keys.append('w')

        self.update(goal)
        return self.keys

    def translate_keys(self, vec: Coordinates):
        """ translates a vector into a key """
        self.keys = []
        if (vec.x == 0 and vec.y == 1):
            self.y += 1
            self.keys.append('s')
        if (vec.x == 0 and vec.y == -1):
            self.y -= 1
            self.keys.append('w')
        if (vec.x == 1 and vec.y == 0):
            self.x += 1
            self.keys.append('d')
        if (vec.x == -1 and vec.y == 0):
            self.x -= 1
            self.keys.append('a')

        return self.keys

    def translate(self, vec: Coordinates):
        """ translates a vector into a key """
        if (vec.x == 0 and vec.y == 1):
            self.y += 1
            self.keys.append('s')
        if (vec.x == 0 and vec.y == -1):
            self.y -= 1
            self.keys.append('w')
        if (vec.x == 1 and vec.y == 0):
            self.x += 1
            self.keys.append('d')
        if (vec.x == -1 and vec.y == 0):
            self.x -= 1
            self.keys.append('a')
        return 0

    def movelevel(self, map, actions):
        self.keys = []
        lastpiece = None
        map2 = Map(str(map))
        for action in actions:
            self.keys.append('1')
            if lastpiece != action[0]:

                self.force_unselect()
                cord = map2.piece_coordinates(action[0])

                map2.move(action[0], action[1])
                self.move(cord[1])
                self.force_select()
                self.translate(action[1])

                lastpiece = action[0]

            else:  # if piece is selected and theres another move for the same piece
                map2.move(action[0], action[1])
                self.translate(action[1])

        return self.keys

    def __str__(self):
        return "cursor(" + str(self.x) + "," + str(self.y) + ")"
