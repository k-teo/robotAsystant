import pygame
import sys
import Node
import os
from datetime import datetime


class MapCreator:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((850, 850))
        pygame.display.set_caption(('MapCreator'))
        self.clock = pygame.time.Clock()
        self.nodes = []
        if os.path.isfile('Nodes.csv') and os.path.isfile('Connections.csv'):
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

                if event.type == pygame.MOUSEBUTTONUP:
                    if not pygame.mouse.get_pressed()[0]:
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
                        print('Zapisano: ' +datetime.now().strftime("%H:%M:%S"))
                        #save data
            self.show()

m = MapCreator()
m.loop()