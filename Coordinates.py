from enum import Enum


class Direction(Enum):
    NORTH = 1
    SOUTH = -1
    EAST = 1
    WEST = -1


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == Direction.NORTH or direction == Direction.SOUTH:
            self.y += direction
        elif direction == Direction.EAST or direction == Direction.WEST:
            self.y += direction
