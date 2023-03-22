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
        self.window = pygame.display.set_mode((850, 850))
        pygame.display.set_caption(('MapCreator'))
        self.clock = pygame.time.Clock()
        self.nodes = []
        if os.path.isfile('Nodes.csv') and os.path.isfile('Connections.csv') and os.path.isfile('Product.csv'):
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
                if int(val[2]) == Product.Side.N.value: self.nodes[int(val[0])].products.append(Product.Product(val[1], Product.Side.N))
                elif int(val[2]) == Product.Side.E.value: self.nodes[int(val[0])].products.append(Product.Product(val[1], Product.Side.E))
                elif int(val[2]) == Product.Side.S.value: self.nodes[int(val[0])].products.append(Product.Product(val[1], Product.Side.S))
                elif int(val[2]) == Product.Side.W.value: self.nodes[int(val[0])].products.append(Product.Product(val[1], Product.Side.W))
            file.close()
        else:
            for y in range(16):
                for x in range(16):
                    self.nodes.append(Node.Node(y*16+x,x,y))
        self.clickedNode = None

    def show(self):
        self.window.fill((255, 255, 255))
        #rysowanie
        for node in self.nodes:
            pygame.draw.circle(self.window,(0,0,0),(node.x * 50 + 25 ,node.y * 50 + 25), 5)
            for c in node.connections:
                pygame.draw.line(self.window,(0,0,0),(node.x * 50 + 25,node.y * 50 + 25),(c.x * 50 + 25,c.y * 50 + 25),3)
            for p in node.products:
                if p.side == Product.Side.N:  self.window.blit(self.font.render(p.name, True, (0, 0, 255)), (node.x * 50 + 25,node.y * 50 + 20 - 5))
                if p.side == Product.Side.E:  self.window.blit(self.font.render(p.name, True, (0, 0, 255)), (node.x * 50 + 25 + 5,node.y * 50 + 20))
                if p.side == Product.Side.S:  self.window.blit(self.font.render(p.name, True, (0, 0, 255)), (node.x * 50 + 25,node.y * 50 + 20 + 5))
                if p.side == Product.Side.W:  self.window.blit(self.font.render(p.name, True, (0, 0, 255)), (node.x * 50 + 25 - 5,node.y * 50 + 20))
        if self.clickedNode is not None:
            pygame.draw.line(self.window, (0, 0, 0), (self.clickedNode.x * 50 + 25, self.clickedNode.y * 50 + 25), pygame.mouse.get_pos(),3)
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
                        distance = abs(self.nodes[0].x * 50 + 25-pygame.mouse.get_pos()[0])+abs(self.nodes[0].y * 50 + 25-pygame.mouse.get_pos()[1])
                        mini = 0
                        for i in range(len(self.nodes)):
                            tempdist = abs(self.nodes[i].x * 50 + 25-pygame.mouse.get_pos()[0])+abs(self.nodes[i].y * 50 + 25-pygame.mouse.get_pos()[1])
                            if tempdist < distance:
                                distance = tempdist
                                mini = i
                        self.clickedNode = self.nodes[mini]
                    if pygame.mouse.get_pressed()[2]:
                        distance = abs(self.nodes[0].x * 50 + 25 - pygame.mouse.get_pos()[0]) + abs(
                            self.nodes[0].y * 50 + 25 - pygame.mouse.get_pos()[1])
                        mini = 0
                        for i in range(len(self.nodes)):
                            tempdist = abs(self.nodes[i].x * 50 + 25 - pygame.mouse.get_pos()[0]) + abs(
                                self.nodes[i].y * 50 + 25 - pygame.mouse.get_pos()[1])
                            if tempdist < distance:
                                distance = tempdist
                                mini = i
                        name = input('Nazwa produktu: ')
                        side = input('Strona: ')
                        print(name+' '+side)
                        if side == 'n' or side == 'N':
                            self.nodes[mini].products.append(Product.Product(name,Product.Side.N))
                        elif side == 'e' or side == 'E':
                            self.nodes[mini].products.append(Product.Product(name,Product.Side.E))
                        elif side == 's' or side == 'S':
                            self.nodes[mini].products.append(Product.Product(name,Product.Side.S))
                        elif side == 'w' or side == 'W':
                            self.nodes[mini].products.append(Product.Product(name,Product.Side.W))
                        else: print('no match')

                if event.type == pygame.MOUSEBUTTONUP:
                    if not pygame.mouse.get_pressed()[0] and self.clickedNode is not None:
                        distance = abs(self.nodes[0].x * 50 + 25 - pygame.mouse.get_pos()[0]) + abs(
                            self.nodes[0].y * 50 + 25 - pygame.mouse.get_pos()[1])
                        mini = 0
                        for i in range(len(self.nodes)):
                            tempdist = abs(self.nodes[i].x * 50 + 25 - pygame.mouse.get_pos()[0]) + abs(
                                self.nodes[i].y * 50 + 25 - pygame.mouse.get_pos()[1])
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
                                file.write(str(node.id) + separator + str(p.name) + separator + str(p.side.value) + '\n')
                        file.close()

                        print('Zapisano: ' +datetime.now().strftime("%H:%M:%S"))
                        #save data
            self.show()

m = MapCreator()
m.loop()