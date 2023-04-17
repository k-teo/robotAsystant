import pygame
import sys
import Node
import os
from datetime import datetime
import Product


class MapCreator:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(None, 20)
        self.window = pygame.display.set_mode((988, 988))
        pygame.display.set_caption(('MapCreator'))
        self.clock = pygame.time.Clock()
        self.nodes = []
        if os.path.isfile('Nodes.csv') and os.path.isfile('Connections.csv') and os.path.isfile('Product.csv'):
            file = open('Nodes.csv')
            for line in file.read().splitlines():
                val = [int(i) for i in line.split(';')]
                self.nodes.append(Node.Node(val[0], val[1], val[2]))
            file.close()
            file = open('Connections.csv')
            for line in file.read().splitlines():
                val = [int(i) for i in line.split(';')]
                self.nodes[val[0]].connections.append(self.nodes[val[1]])
                self.nodes[val[1]].connections.append(self.nodes[val[0]])
            file.close()
            file = open('Product.csv')
            for line in file.read().splitlines():
                val = line.split(';')
                self.nodes[int(val[0])].products.append(Product.Product(val[1],self.nodes[int(val[0])]))
            file.close()
        else:
            for y in range(26):
                for x in range(26):
                    self.nodes.append(Node.Node(y * 26 + x, x, y))
        self.clickedNode = None

    def show(self):
        self.window.fill((255, 255, 255))
        #rysowanie
        for node in self.nodes:
            pygame.draw.circle(self.window,(0,0,0),(node.x * 37 + 13 ,node.y * 37 + 13), 5)
            for c in node.connections:
                pygame.draw.line(self.window,(0,0,0),(node.x * 37 + 13,node.y * 37 + 13),(c.x * 37 + 13,c.y * 37 + 13),3)
            for p in node.products:
                self.window.blit(self.font.render(p.name, True, (0, 0, 255)), (node.x * 37 + 13 - 13,node.y * 37 + 13 - 13))
        if self.clickedNode is not None:
            pygame.draw.line(self.window, (0, 0, 0), (self.clickedNode.x * 37 + 13, self.clickedNode.y * 37 + 13), pygame.mouse.get_pos(),3)
        pygame.display.flip()
        self.clock.tick(60)

    def loop(self):
        mousePressed = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        distance = abs(self.nodes[0].x * 37 + 13-pygame.mouse.get_pos()[0])+abs(self.nodes[0].y * 37 + 13-pygame.mouse.get_pos()[1])
                        mini = 0
                        for i in range(len(self.nodes)):
                            tempdist = abs(self.nodes[i].x * 37 + 13-pygame.mouse.get_pos()[0])+abs(self.nodes[i].y * 37 + 13-pygame.mouse.get_pos()[1])
                            if tempdist < distance:
                                distance = tempdist
                                mini = i
                        self.clickedNode = self.nodes[mini]
                    if pygame.mouse.get_pressed()[2]:
                        distance = abs(self.nodes[0].x * 37 + 13 - pygame.mouse.get_pos()[0]) + abs(
                            self.nodes[0].y * 37 + 13 - pygame.mouse.get_pos()[1])
                        mini = 0
                        for i in range(len(self.nodes)):
                            tempdist = abs(self.nodes[i].x * 37 + 13 - pygame.mouse.get_pos()[0]) + abs(
                                self.nodes[i].y * 37 + 13 - pygame.mouse.get_pos()[1])
                            if tempdist < distance:
                                distance = tempdist
                                mini = i
                        name = input('Nazwa produktu: ')
                        self.nodes[mini].products.append(Product.Product(name,self.nodes[mini]))

                if event.type == pygame.MOUSEBUTTONUP:
                    if not pygame.mouse.get_pressed()[0] and self.clickedNode is not None:
                        distance = abs(self.nodes[0].x * 37 + 13 - pygame.mouse.get_pos()[0]) + abs(
                            self.nodes[0].y * 37 + 13 - pygame.mouse.get_pos()[1])
                        mini = 0
                        for i in range(len(self.nodes)):
                            tempdist = abs(self.nodes[i].x * 37 + 13 - pygame.mouse.get_pos()[0]) + abs(
                                self.nodes[i].y * 37 + 13 - pygame.mouse.get_pos()[1])
                            if tempdist < distance:
                                distance = tempdist
                                mini = i
                        if mini != self.clickedNode.id:
                            isin = True
                            for c in self.clickedNode.connections:
                                if c.id == mini: isin = False
                            if isin:
                                self.clickedNode.connections.append(self.nodes[mini])
                                self.nodes[mini].connections.append((self.nodes[self.clickedNode.id]))
                            else:
                                self.clickedNode.connections.remove(self.nodes[mini])
                                self.nodes[mini].connections.remove((self.nodes[self.clickedNode.id]))
                        self.clickedNode = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                    if event.key == pygame.K_DOWN:
                        pass
                    if event.key == pygame.K_LEFT:
                        pass
                    if event.key == pygame.K_RETURN:
                        separator = ';'
                        file = open('Nodes.csv','w')
                        for node in self.nodes:
                            file.write(str(node.id)+separator+str(node.x)+separator+str(node.y)+'\n')
                        file.close()
                        file = open('Connections.csv', 'w')
                        for node in self.nodes:
                            for c in node.connections:
                                if c.id > node.id:
                                    file.write(str(node.id) + separator + str(c.id) + '\n')
                        file.close()
                        file = open('Product.csv', 'w')
                        for node in self.nodes:
                            for p in node.products:
                                file.write(str(node.id) + separator + str(p.name) + '\n')
                        file.close()

                        print('Zapisano: ' +datetime.now().strftime("%H:%M:%S"))
                        #save data
            self.show()

m = MapCreator()
m.loop()

def mapnegation():
    nodes = []
    negationNodes = []
    if os.path.isfile('Nodes.csv') and os.path.isfile('Connections.csv') and os.path.isfile('Product.csv'):
        file = open('Nodes.csv')
        for line in file.read().splitlines():
            val = [int(i) for i in line.split(';')]
            nodes.append(Node.Node(val[0], val[1], val[2]))
            negationNodes.append(Node.Node(val[0], val[1], val[2]))
        file.close()
        file = open('Connections.csv')
        for line in file.read().splitlines():
            val = [int(i) for i in line.split(';')]
            nodes[val[0]].connections.append(nodes[val[1]])
            nodes[val[1]].connections.append(nodes[val[0]])
        file.close()
    else:
        print('error')
        return

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            notconnected = True
            for k in nodes[i].connections:
                if k.id == nodes[j].id:
                    notconnected = False
            if i != j and abs(nodes[i].x-nodes[j].x) + abs(nodes[i].y-nodes[j].y) == 1 and notconnected:
                negationNodes[i].connections.append(negationNodes[j])
                negationNodes[j].connections.append(negationNodes[i])
    file = open('Paths.csv', 'w')
    for node in negationNodes:
        for c in node.connections:
            if c.id > node.id:
                file.write(str(node.id) + ";" + str(c.id) + '\n')
    file.close()

mapnegation()