import pygame
import sys
import Node
import os
from datetime import datetime
import Product
import random
import calculatePath
import textComparator


class Map:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(None, 20)
        self.fontSmall = pygame.font.Font(None, 16)
        self.window = pygame.display.set_mode((988+148, 988))
        pygame.display.set_caption(('MapCreator'))
        self.clock = pygame.time.Clock()
        self.nodes = []
        self.products = []
        self.destinationProducts = []
        self.productTextRect = pygame.Rect(988 - 37 + 13 + 13, 13+13, 148 - 13, 40)
        self.productTextActive = False
        self.productTextColor = (225, 225, 225)
        self.productText = ''
        self.path = []
        self.textComp = textComparator.TextComparator()
        if os.path.isfile('Nodes.csv') and os.path.isfile('Connections.csv') and os.path.isfile('Product.csv') and os.path.isfile('Paths.csv'):
            file = open('Nodes.csv')
            for line in file.read().splitlines():
                val = [int(i) for i in line.split(';')]
                tempnode = Node.Node(val[0])
                tempnode.set_coordinates(val[1], val[2])
                self.nodes.append(tempnode)
            file.close()
            file = open('Connections.csv')
            for line in file.read().splitlines():
                val = [int(i) for i in line.split(';')]
                node1 = None
                node2 = None
                for node in self.nodes:
                    if node.id == val[0]:
                        node1 = node
                for node in self.nodes:
                    if node.id == val[1]:
                        node2 = node
                node1.connections.add(node2)
                node2.connections.add(node1)
            file.close()
            file = open('Product.csv')
            for line in file.read().splitlines():
                val = line.split(';')
                node1 = None
                for node in self.nodes:
                    if node.id == int(val[0]):
                        node1 = node
                product = Product.Product(val[1],self.nodes[int(val[0])])
                node1.products.add(product)
                self.products.append(product)
            file.close()
            file = open('Paths.csv')
            for line in file.read().splitlines():
                val = [int(i) for i in line.split(';')]
                node1 = None
                node2 = None
                for node in self.nodes:
                    if node.id == val[0]:
                        node1 = node
                for node in self.nodes:
                    if node.id == val[1]:
                        node2 = node
                node1.paths.add(node2)
                node2.paths.add(node1)
            file.close()
        else:
            for y in range(26):
                for x in range(26):
                    self.nodes.append(Node.Node(y*26+x,x,y))
        self.currentNode = random.choice(self.nodes)


    def show(self):
        self.window.fill((255, 255, 255))
        #rysowanie
        pygame.draw.rect(self.window, (225, 225, 225), (988 - 37 + 13, 13, 148 + 13, 988 - 37))
        pygame.draw.rect(self.window, self.productTextColor, self.productTextRect)
        pygame.draw.rect(self.window, (0,0,0), self.productTextRect,1)
        for i in range(len(self.destinationProducts)):
            #napis produktu
            pygame.draw.rect(self.window, (245, 245, 245), pygame.Rect(988 - 37 + 13 + 13, 13+13+40+5+i*25, 81, 20))
            pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(988 - 37 + 13 + 13, 13+13+40+5+i*25, 81, 20), 1)
            self.window.blit(self.fontSmall.render(self.destinationProducts[i].name, True, (0, 0, 0)),
                             (988 - 37 + 13 + 13 +5, 13+13+40+5+i*25 + 4))
            #wyznacz trasę
            pygame.draw.rect(self.window, (245, 245, 245),
                             pygame.Rect(988 - 37 + 13 + 13 + 83, 13 + 13 + 40 + 5 + i * 25, 25, 20))
            pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(988 - 37 + 13 + 13+ 83, 13 + 13 + 40 + 5 + i * 25, 25, 20),
                             1)
            self.window.blit(self.fontSmall.render('->', True, (0, 0, 225)),
                             (988 - 37 + 13 + 13 + 5 + 84, 13 + 13 + 40 + 5 + i * 25 + 4))
            #usuń
            pygame.draw.rect(self.window, (245, 245, 245),
                             pygame.Rect(988 - 37 + 13 + 13 + 83 + 27, 13 + 13 + 40 + 5 + i * 25, 25, 20))
            pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(988 - 37 + 13 + 13 + 83 + 27, 13 + 13 + 40 + 5 + i * 25, 25, 20),
                             1)
            self.window.blit(self.fontSmall.render('X', True, (255, 0, 0)),
                             (988 - 37 + 13 + 13 + 5 + 84 + 27, 13 + 13 + 40 + 5 + i * 25 + 4))
        #Droga po wszystkich
        pygame.draw.rect(self.window, (245, 245, 245),
                         pygame.Rect(988 - 37 + 13 + 13, 13 + 13 + 40 + 5 + len(self.destinationProducts) * 25, 135, 20))
        pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(988 - 37 + 13 + 13, 13 + 13 + 40 + 5 + len(self.destinationProducts) * 25, 135, 20), 1)
        self.window.blit(self.fontSmall.render('Wszystkie produkty', True, (0, 0, 0)),
                         (988 - 37 + 13 + 13 + 5, 13 + 13 + 40 + 5 + len(self.destinationProducts) * 25 + 4))

        for node in self.nodes:
            for c in node.paths:
                pygame.draw.line(self.window,(224,224,224),(node.x * 37 + 13,node.y * 37 + 13),(c.x * 37 + 13,c.y * 37 + 13),5)
        for node in self.nodes:
            #pygame.draw.circle(self.window,(0,0,0),(node.x * 37 + 13 ,node.y * 37 + 13), 5)
            for c in node.connections:
                pygame.draw.line(self.window,(0,0,0),(node.x * 37 + 13,node.y * 37 + 13),(c.x * 37 + 13,c.y * 37 + 13),3)
            for p in node.products:
                self.window.blit(self.font.render(p.name, True, (0, 0, 255)), (node.x * 37 + 13 - 13,node.y * 37 + 13 - 13))
        for p in range(len(self.path)-1):
            pygame.draw.line(self.window, (255, 0, 0), (self.path[p].x * 37 + 13, self.path[p].y * 37 + 13),
                             (self.path[p+1].x * 37 + 13, self.path[p+1].y * 37 + 13), 3)
        pygame.draw.circle(self.window, (255, 0, 0), (self.currentNode.x * 37 + 13, self.currentNode.y * 37 + 13), 7)

        self.window.blit(self.font.render(self.productText, True, (0, 0, 0)), (self.productTextRect.x, self.productTextRect.y + 10))
        pygame.display.flip()
        self.clock.tick(60)

    def __move(self,x,y):
        for node in self.currentNode.paths:
            if self.currentNode.x - node.x == x and self.currentNode.y - node.y == y:
                self.currentNode = node

    def loop(self):
        mousePressed = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.productTextRect.collidepoint(event.pos):
                        self.productTextActive = True
                        self.productTextColor = (255, 255, 255)
                    else:
                        self.productTextActive = False
                        self.productTextColor = (240, 240, 240)
                    if pygame.Rect(988 - 37 + 13 + 13, 13 + 13 + 40 + 5 + len(self.destinationProducts) * 25, 135, 20).collidepoint(event.pos):
                        print('wszystkie produkty')

                    for i in range(len(self.destinationProducts)):
                        if pygame.Rect(988 - 37 + 13 + 13+ 83, 13 + 13 + 40 + 5 + i * 25, 25, 20).collidepoint(event.pos):
                            path = calculatePath.calculate_path2(self.currentNode, self.destinationProducts[i].node)
                            self.path = path
                            break
                        if pygame.Rect(988 - 37 + 13 + 13 + 83 + 27, 13 + 13 + 40 + 5 + i * 25, 25, 20).collidepoint(event.pos):
                            self.destinationProducts.remove(self.destinationProducts[i])
                            break


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.__move(0,1)
                    if event.key == pygame.K_RIGHT:
                        self.__move(-1,0)
                    if event.key == pygame.K_DOWN:
                        self.__move(0,-1)
                    if event.key == pygame.K_LEFT:
                        self.__move(1,0)

                    if event.key == pygame.K_BACKSPACE:
                        if self.productText != '':
                            self.productText = self.productText[:-1]
                    if str(event.unicode).isalpha() and self.productTextActive and len(self.productText)<10:
                        self.productText += event.unicode
                    if event.key == pygame.K_RETURN:
                        destination = None
                        for prod in self.products:
                            if self.textComp.compare(self.productText,prod.name):
                                destination = prod
                        if destination is not None:
                            if destination not in self.destinationProducts:
                                self.destinationProducts.append(destination)
                        self.productText = ''

            self.show()

if __name__ == "__main__":
    m = Map()
    m.loop()