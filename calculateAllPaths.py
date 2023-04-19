import os
import Node
import Product

def calculateAllPaths():
    nodes = []
    products = []
    if os.path.isfile('Nodes.csv') and os.path.isfile('Connections.csv') and os.path.isfile(
            'Product.csv') and os.path.isfile('Paths.csv'):
        file = open('Nodes.csv')
        for line in file.read().splitlines():
            val = [int(i) for i in line.split(';')]
            tempnode = Node.Node(val[0])
            tempnode.set_coordinates(val[1], val[2])
            nodes.append(tempnode)
        file.close()
        file = open('Product.csv')
        for line in file.read().splitlines():
            val = line.split(';')
            product = Product.Product(val[1], nodes[int(val[0])])
            products.append(product)
        file.close()
        file = open('Paths.csv')
        for line in file.read().splitlines():
            val = [int(i) for i in line.split(';')]
            node1 = None
            node2 = None
            for node in nodes:
                if node.id == val[0]:
                    node1 = node
            for node in nodes:
                if node.id == val[1]:
                    node2 = node
            node1.paths.add(node2)
            node2.paths.add(node1)
        file.close()

        data = {}
        for i in products:
            data[i.name]=[]
            for j in range(len(nodes)):
                data[i.name][j]=0

    for product in products:
        queue = [(product.node, [product.node], 0)]
        while queue:
            (vertex, path, distance) = queue.pop(0)
            for v in vertex.paths - set(path):
                if v == destination:
                    yield path + [v]
                else:
                    queue.append((v, path + [v]))