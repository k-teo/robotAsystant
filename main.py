import json
import plotly.graph_objects as go

def initMapFromJson():
    f = open('map.json')
    return json.load(f)


def visualize_map(map):
    fig = go.Figure()

    add_shelf_shapes(fig, map)

    fig.update_xaxes(range=[0, map["size"]["length"]])
    fig.update_yaxes(range=[0, map["size"]["width"]])
    fig.show()


def add_shelf_shapes(fig, map):
    for shelf in map["shelfs"]:
        x = []
        y = []
        x.append(shelf["distancefromleft"])
        y.append(shelf["distancefrombottom"])
        x.append(shelf["distancefromleft"] + shelf["length"])
        y.append(shelf["distancefrombottom"])
        x.append(shelf["distancefromleft"] + shelf["length"])
        y.append(shelf["distancefrombottom"] + shelf["width"])
        x.append(shelf["distancefromleft"])
        y.append(shelf["distancefrombottom"] + shelf["width"])
        fig.add_trace(go.Scatter(x=x, y=y, fill="toself"))


def init_products():
    f = open('products.json')
    return json.load(f)["products"]


def get_products_names(products):
    products_names = []
    for product in products:
        print(product["name"])
        products_names.append(product["name"])
    return products_names


if __name__ == '__main__':
    map = initMapFromJson()
    products = init_products()
    products_names = get_products_names(products)
    visualize_map(map)

