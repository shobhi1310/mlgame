import pygame
import random

class Node():

    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
N = 100
R = 6
radius = 5
color = (0,0,255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True

list = []

for i in range(100):
    list.append(Node(random.randint(0,500),random.randint(0,500),random.randint(0,2)))

for i in range(100):
        pygame.draw.circle(screen, color, (list[i].x, list[i].y), radius)

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    pygame.display.update()
