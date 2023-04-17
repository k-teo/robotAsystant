from Node import Node


class AdjacencyList:
    def __init__(self, size):
        self.size = size
        self.graph = {}
        self.products = {}
        self.init_graph()

    def init_graph(self):
        for id in range(self.size):
            self.graph[id] = Node(id)

    def add_edge(self, v1, v2):
        self.graph[v1].add_connection(v2)
        self.graph[v2].add_connection(v1)

    def set_coordinates(self, node_id, x, y):
        self.graph[node_id].set_coordinates(x, y)

    def set_product(self, node_id, product):
        self.graph[node_id].add_product(product)
        self.products[product] = node_id

    def get_product_destination(self, product_name):
        return self.products[product_name]


