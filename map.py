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
        self.window = pygame.display.set_mode((988 + 148, 988))
        pygame.display.set_caption(('MapCreator'))
        self.clock = pygame.time.Clock()
        self.nodes = []
        self.products = []
        self.destinationProducts = []
        self.productTextRect = pygame.Rect(988 - 37 + 13 + 13, 13 + 13, 148 - 13, 40)
        self.productTextActive = False
        self.productTextColor = (225, 225, 225)
        self.productText = ''
        self.path = []
        self.destination = -2
        self.textComp = textComparator.TextComparator()
        if os.path.isfile('Nodes.csv') and os.path.isfile('Connections.csv') and os.path.isfile(
                'Product.csv') and os.path.isfile('Paths.csv'):
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
                product = Product.Product(val[1], self.nodes[int(val[0])])
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
                    self.nodes.append(Node.Node(y * 26 + x, x, y))
        self.currentNode = random.choice(self.nodes)

    def show(self):
        self.window.fill((255, 255, 255))
        # rysowanie
        pygame.draw.rect(self.window, (225, 225, 225), (988 - 37 + 13, 13, 148 + 13, 988 - 37))
        pygame.draw.rect(self.window, self.productTextColor, self.productTextRect)
        pygame.draw.rect(self.window, (0, 0, 0), self.productTextRect, 1)
        # strzalka
        pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(988 - 37 + 13 + 13 + 20, 988 - 135, 100, 100))
        pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(988 - 37 + 13 + 13 + 20, 988 - 135, 100, 100), 1)
        if len(self.path)>1:
            if self.currentNode.y > self.path[1].y:
                # up
                self.__draw_arrow(self.window,pygame.Vector2(988 - 37 + 13 + 13 + 20 + 50,988 - 135 + 100),pygame.Vector2(988 - 37 + 13 + 13 + 20 + 50,988 - 135),(0,0,0))
            elif self.currentNode.y < self.path[1].y:
                # down
                self.__draw_arrow(self.window,pygame.Vector2(988 - 37 + 13 + 13 + 20 + 50,988 - 135),pygame.Vector2(988 - 37 + 13 + 13 + 20 + 50,988 - 135 + 100),(0,0,0))
            elif self.currentNode.x < self.path[1].x:
                # left
                self.__draw_arrow(self.window,pygame.Vector2(988 - 37 + 13 + 13 + 20,988 - 135 + 50),pygame.Vector2(988 - 37 + 13 + 13 + 20 + 100,988 - 135 + 50),(0,0,0))
            elif self.currentNode.x > self.path[1].x:
                # right
                self.__draw_arrow(self.window,pygame.Vector2(988 - 37 + 13 + 13 + 20 + 100,988 - 135 + 50),pygame.Vector2(988 - 37 + 13 + 13 + 20,988 - 135 + 50),(0,0,0))

        for i in range(len(self.destinationProducts)):
            # napis produktu
            pygame.draw.rect(self.window, (245, 245, 245),
                             pygame.Rect(988 - 37 + 13 + 13, 13 + 13 + 40 + 5 + i * 25, 81, 20))
            pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(988 - 37 + 13 + 13, 13 + 13 + 40 + 5 + i * 25, 81, 20),
                             1)
            self.window.blit(self.fontSmall.render(self.destinationProducts[i].name, True, (0, 0, 0)),
                             (988 - 37 + 13 + 13 + 5, 13 + 13 + 40 + 5 + i * 25 + 4))
            # wyznacz trasę
            pygame.draw.rect(self.window, (245, 245, 245),
                             pygame.Rect(988 - 37 + 13 + 13 + 83, 13 + 13 + 40 + 5 + i * 25, 25, 20))
            pygame.draw.rect(self.window, (0, 0, 0),
                             pygame.Rect(988 - 37 + 13 + 13 + 83, 13 + 13 + 40 + 5 + i * 25, 25, 20),
                             1)
            self.window.blit(self.fontSmall.render('->', True, (0, 0, 225)),
                             (988 - 37 + 13 + 13 + 5 + 84, 13 + 13 + 40 + 5 + i * 25 + 4))
            # usuń
            pygame.draw.rect(self.window, (245, 245, 245),
                             pygame.Rect(988 - 37 + 13 + 13 + 83 + 27, 13 + 13 + 40 + 5 + i * 25, 25, 20))
            pygame.draw.rect(self.window, (0, 0, 0),
                             pygame.Rect(988 - 37 + 13 + 13 + 83 + 27, 13 + 13 + 40 + 5 + i * 25, 25, 20),
                             1)
            self.window.blit(self.fontSmall.render('X', True, (255, 0, 0)),
                             (988 - 37 + 13 + 13 + 5 + 84 + 27, 13 + 13 + 40 + 5 + i * 25 + 4))
        # Droga po wszystkich
        pygame.draw.rect(self.window, (245, 245, 245),
                         pygame.Rect(988 - 37 + 13 + 13, 13 + 13 + 40 + 5 + len(self.destinationProducts) * 25, 135,
                                     20))
        pygame.draw.rect(self.window, (0, 0, 0),
                         pygame.Rect(988 - 37 + 13 + 13, 13 + 13 + 40 + 5 + len(self.destinationProducts) * 25, 135,
                                     20), 1)
        self.window.blit(self.fontSmall.render('Wszystkie produkty', True, (0, 0, 0)),
                         (988 - 37 + 13 + 13 + 5, 13 + 13 + 40 + 5 + len(self.destinationProducts) * 25 + 4))

        for node in self.nodes:
            for c in node.paths:
                pygame.draw.line(self.window, (224, 224, 224), (node.x * 37 + 13, node.y * 37 + 13),
                                 (c.x * 37 + 13, c.y * 37 + 13), 5)
        for node in self.nodes:
            # pygame.draw.circle(self.window,(0,0,0),(node.x * 37 + 13 ,node.y * 37 + 13), 5)
            for c in node.connections:
                pygame.draw.line(self.window, (0, 0, 0), (node.x * 37 + 13, node.y * 37 + 13),
                                 (c.x * 37 + 13, c.y * 37 + 13), 3)
            for p in node.products:
                self.window.blit(self.font.render(p.name, True, (0, 0, 255)),
                                 (node.x * 37 + 13 - 13, node.y * 37 + 13 - 13))
        for p in range(len(self.path) - 2,-1,-1):
            pygame.draw.line(self.window, (255, int(p*224/len(self.path)), int(p*224/len(self.path))), (self.path[p].x * 37 + 13, self.path[p].y * 37 + 13),
                             (self.path[p + 1].x * 37 + 13, self.path[p + 1].y * 37 + 13), 3)
        pygame.draw.circle(self.window, (255, 0, 0), (self.currentNode.x * 37 + 13, self.currentNode.y * 37 + 13), 7)

        self.window.blit(self.font.render(self.productText, True, (0, 0, 0)),
                         (self.productTextRect.x, self.productTextRect.y + 10))
        pygame.display.flip()
        self.clock.tick(60)

    def __move(self, x, y):
        for node in self.currentNode.paths:
            if self.currentNode.x - node.x == x and self.currentNode.y - node.y == y:
                self.currentNode = node
        if self.destination > -2:
            if len(self.path) > 1:
                if self.path[1] == self.currentNode:
                    self.path.remove(self.path[0])
                else:
                    if self.destination == -1:
                        path = calculatePath.multipleProducts(self.currentNode,
                                                              [i.node for i in self.destinationProducts])
                        self.path = path
                    else:
                        path = calculatePath.calculate_path2(self.currentNode, self.destinationProducts[self.destination].node)
                        self.path = path



            else:
                self.path = []
                self.destination = -2

        for i in self.destinationProducts:
            if i.node == self.currentNode:
                self.destinationProducts.remove(i)
                if self.destination == -1:
                    path = calculatePath.multipleProducts(self.currentNode,
                                                          [i.node for i in self.destinationProducts])
                    self.path = path


    def __draw_arrow(
            self,
            surface: pygame.Surface,
            start: pygame.Vector2,
            end: pygame.Vector2,
            color: pygame.Color,
            body_width: int = 2,
            head_width: int = 20,
            head_height: int = 25,
    ):
        """Draw an arrow between start and end with the arrow head at the end.

        Args:
            surface (pygame.Surface): The surface to draw on
            start (pygame.Vector2): Start position
            end (pygame.Vector2): End position
            color (pygame.Color): Color of the arrow
            body_width (int, optional): Defaults to 2.
            head_width (int, optional): Defaults to 4.
            head_height (float, optional): Defaults to 2.
        """
        arrow = start - end
        angle = arrow.angle_to(pygame.Vector2(0, -1))
        body_length = arrow.length() - head_height

        # Create the triangle head around the origin
        head_verts = [
            pygame.Vector2(0, head_height / 2),  # Center
            pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
            pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
        ]
        # Rotate and translate the head into place
        translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
        for i in range(len(head_verts)):
            head_verts[i].rotate_ip(-angle)
            head_verts[i] += translation
            head_verts[i] += start

        pygame.draw.polygon(surface, color, head_verts)

        # Stop weird shapes when the arrow is shorter than arrow head
        if arrow.length() >= head_height:
            # Calculate the body rect, rotate and translate into place
            body_verts = [
                pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
                pygame.Vector2(body_width / 2, body_length / 2),  # Topright
                pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
                pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
            ]
            translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
            for i in range(len(body_verts)):
                body_verts[i].rotate_ip(-angle)
                body_verts[i] += translation
                body_verts[i] += start

            pygame.draw.polygon(surface, color, body_verts)

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
                    if pygame.Rect(988 - 37 + 13 + 13, 13 + 13 + 40 + 5 + len(self.destinationProducts) * 25, 135,
                                   20).collidepoint(event.pos):
                        path = calculatePath.multipleProducts(self.currentNode,
                                                              [i.node for i in self.destinationProducts])
                        self.path = path
                        self.destination = -1

                    for i in range(len(self.destinationProducts)):
                        if pygame.Rect(988 - 37 + 13 + 13 + 83, 13 + 13 + 40 + 5 + i * 25, 25, 20).collidepoint(
                                event.pos):
                            path = calculatePath.calculate_path2(self.currentNode, self.destinationProducts[i].node)
                            self.path = path
                            self.destination = i
                            break
                        if pygame.Rect(988 - 37 + 13 + 13 + 83 + 27, 13 + 13 + 40 + 5 + i * 25, 25, 20).collidepoint(
                                event.pos):
                            self.destinationProducts.remove(self.destinationProducts[i])
                            if self.destination == i:
                                self.destination = -2
                            break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.__move(0, 1)
                    if event.key == pygame.K_RIGHT:
                        self.__move(-1, 0)
                    if event.key == pygame.K_DOWN:
                        self.__move(0, -1)
                    if event.key == pygame.K_LEFT:
                        self.__move(1, 0)

                    if event.key == pygame.K_BACKSPACE:
                        if self.productText != '':
                            self.productText = self.productText[:-1]
                    if str(event.unicode).isalpha() and self.productTextActive and len(self.productText) < 10:
                        self.productText += event.unicode
                    if event.key == pygame.K_RETURN:
                        destinations = []
                        for prod in self.products:
                            if self.textComp.is_the_same(self.productText, prod.name):
                                destinations = [prod]
                                break
                            if self.textComp.compare(self.productText, prod.name):
                                destinations.append(prod)
                        for destination in destinations:
                            if destination not in self.destinationProducts:
                                self.destinationProducts.append(destination)
                        self.productText = ''

            self.show()



if __name__ == "__main__":
    m = Map()
    m.loop()
