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

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
start_x = 20
start_y = 20
end = 501
rows = 20
cols = 30
width = 5
height = 5
R = 8
radius = 10

blue = (0,0,255)
red = (255,0,0)
dull = (69, 79, 70)
white = (255,255,255)
black = (0,0,0)

color=[dull,blue,red]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True

#initialising grid
grid = []
y = start_y
for i in range(rows):
    r = []
    x = start_x
    for j in range(cols):
        r.append(Node(x,y,dull))
        x += 2*radius + width
    grid.append(r)
    y += 2*radius + height

#coloring blue
for i in range(int(R/2)):
    x = random.randint(0,rows-1)
    y = random.randint(0,cols-1)
    grid[x][y].color = blue

#coloring red
for i in range(int(R/2)):
    check = True
    while(check):
        x = random.randint(0,rows-1)
        y = random.randint(0,cols-1)
        if grid[x][y].color == blue:
            x = random.randint(0,rows-1)
            y = random.randint(0,cols-1)
        else:
            grid[x][y].color = red
            check = False


# print(grid)

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = screen.get_at(pygame.mouse.get_pos()) == dull
            if click == 1:
                X = pygame.mouse.get_pos()[0]
                Y = pygame.mouse.get_pos()[1]
                
                for i in range(rows):
                    for j in range(cols):
                        if((X-grid[i][j].x)**2 + (Y-grid[i][j].y)**2 - radius**2) <= 0:
                            print(i)
                            print(j)
                            grid[i][j].color = blue
                            # pygame.display.update()
                            break
                        
    #drawing on the screen
    for row in grid:
        for node in row:
            pygame.draw.circle(screen, node.color, (node.x, node.y), radius)
            pygame.draw.circle(screen, white, (node.x, node.y), radius, 1)

    pygame.display.flip()
