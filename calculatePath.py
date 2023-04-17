from AdjacencyList import AdjacencyList


def get_adjacency_list():
    file = open('Nodes.csv')
    adjacency_list = AdjacencyList(len(file.read().splitlines()))
    file.close()
    file = open('Nodes.csv')
    for line in file.read().splitlines():
        val = [int(i) for i in line.split(';')]
        adjacency_list.set_coordinates(val[0], val[1], val[2])
    file.close()

    file = open('Product.csv')
    for line in file.read().splitlines():
        val = [i for i in line.split(';')]
        adjacency_list.set_product(int(val[0]), val[1].lower())
    file.close()

    file = open('Paths.csv')
    for line in file.read().splitlines():
        val = [int(i) for i in line.split(';')]
        adjacency_list.add_edge(val[0], val[1])

    file.close()

    return adjacency_list


def get_product_name():
    print("type product")
    return input().lower()


def calculate_path(graph, start, destination):
    try:
        return next(bfs(graph, start, destination))
    except StopIteration:
        return None


def bfs(graph, start, destination):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for v in graph[vertex].connections - set(path):
            if v == destination:
                yield path + [v]
            else:
                queue.append((v, path + [v]))

def calculate_path2(start, destination):
    try:
        return next(bfs2(start, destination))
    except StopIteration:
        return None

def bfs2(start, destination):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for v in vertex.paths - set(path):
            if v == destination:
                yield path + [v]
            else:
                queue.append((v, path + [v]))


'''try:
    adjacency_list = get_adjacency_list()
    destination = adjacency_list.get_product_destination(get_product_name())
    path = calculate_path(adjacency_list.graph, 1, destination)
    print(path)
except:
    print("Could not find the product")'''
