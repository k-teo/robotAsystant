class Node:

    def __init__(self, id):
        self.id = id
        self.x = None
        self.y = None
        self.connections = set()
        self.paths = set()
        self.products = set()
        self.distance = 0

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y

    def add_connection(self, connection_id):
        self.connections.add(connection_id)

    def add_product(self, product):
        self.products.add(product)
