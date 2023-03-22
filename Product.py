from enum import Enum

class Side(Enum):
    N = 1
    E = 2
    S = 3
    W = 4

class Product:
    def __init__(self, name, side:Side):
        self.side = side
        self.name = name