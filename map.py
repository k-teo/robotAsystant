import pygame
import sys
import Node
import os
from datetime import datetime
import Product


class Map:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(None, 20)
        self.window = pygame.display.set_mode((988, 988))
        pygame.display.set_caption(('MapCreator'))
        self.clock = pygame.time.Clock()
        self.nodes = []
        if os.path.isfile('Nodes.csv') and os.path.isfile('Connections.csv') and os.path.isfile('Product.csv') and os.path.isfile('Paths.csv'):
            file = open('Nodes.csv')
            for line in file.read().splitlines():
                val = [int(i) for i in line.split(';')]
                self.nodes.append(Node.Node(val[0],val[1],val[2]))
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
            file = open('Paths.csv')
            for line in file.read().splitlines():
                val = [int(i) for i in line.split(';')]
                self.nodes[val[0]].paths.append(self.nodes[val[1]])
                self.nodes[val[1]].paths.append(self.nodes[val[0]])
            file.close()
        else:
            for y in range(26):
                for x in range(26):
                    self.nodes.append(Node.Node(y*26+x,x,y))
        self.clickedNode = None

    def show(self):
        self.window.fill((255, 255, 255))
        #rysowanie
        for node in self.nodes:
            for c in node.paths:
                pygame.draw.line(self.window,(224,224,224),(node.x * 37 + 13,node.y * 37 + 13),(c.x * 37 + 13,c.y * 37 + 13),5)
        for node in self.nodes:
            #pygame.draw.circle(self.window,(0,0,0),(node.x * 37 + 13 ,node.y * 37 + 13), 5)
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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                    if event.key == pygame.K_DOWN:
                        pass
                    if event.key == pygame.K_LEFT:
                        pass
            self.show()

m = Map()
m.loop()