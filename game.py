import pygame
import random
from collections import Counter
import math

class Node():

    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color

def knn(grid, query_node, k, distance_fn, choice_fn):
    neighbor_distances_and_indices = []
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if( grid[i][j].x == query_node.x and grid[i][j].y == query_node.y):
                pass
            elif(grid[i][j].color > 0):
                distance = distance_fn(grid[i][j],query_node)
                neighbor_distances_and_indices.append((distance,i,j))

    
    sorted_neighbor_distances_and_indices = sorted(neighbor_distances_and_indices)
    
    k_nearest_distances_and_indices = sorted_neighbor_distances_and_indices[:k]
    
    k_nearest_labels = [grid[i][j].color for distance, i, j in k_nearest_distances_and_indices]

    return choice_fn(k_nearest_labels)

def mean(labels):
    return sum(labels) / len(labels)

def mode(labels):
    # print(labels)
    # print(Counter(labels).most_common(1))
    return Counter(labels).most_common(1)[0][0]

def euclidean_distance(point1, point2):
    sum_squared_distance = 0
    sum_squared_distance += math.pow(point1.x - point2.x, 2)
    sum_squared_distance += math.pow(point1.y - point2.y, 2)
    return math.sqrt(sum_squared_distance)


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
start_x = 60
start_y = 80
end = 501
rows = 20
cols = 30
width = 5
height = 5
R = 8
radius = 10
r_count = int(R/2)
b_count = int(R/2)

blue = (0,0,255)
red = (255,0,0)
dull = (69, 79, 70)
white = (255,255,255)
black = (0,0,0)

color=[dull,blue,red]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True


def red_count(r_count):
    font = pygame.font.SysFont('comicsansms', 40)
    text = font.render("Reds: "+str(r_count), True, red)
    screen.blit(text,(10,0))

def blue_count(r_count):
    font = pygame.font.SysFont('comicsansms', 40)
    text = font.render("Blues: "+str(b_count), True, blue)
    screen.blit(text,(800,0))

#initialising grid
grid = []
y = start_y
for i in range(rows):
    r = []
    x = start_x
    for j in range(cols):
        r.append(Node(x,y,0))
        x += 2*radius + width
    grid.append(r)
    y += 2*radius + height

#coloring blue
for i in range(int(R/2)):
    x = random.randint(0,rows-1)
    y = random.randint(0,cols-1)
    grid[x][y].color = 1

#coloring red
for i in range(int(R/2)):
    check = True
    while(check):
        x = random.randint(0,rows-1)
        y = random.randint(0,cols-1)
        if grid[x][y].color == 1:
            x = random.randint(0,rows-1)
            y = random.randint(0,cols-1)
        else:
            grid[x][y].color = 2
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
                            # print(i)
                            # print(j)
                            grid[i][j].color = knn(grid,grid[i][j],k=3,distance_fn=euclidean_distance, choice_fn=mode)
                            if(grid[i][j].color == 1):
                                b_count += 1
                            else:
                                r_count += 1
                            # pygame.display.update()
                            break
    screen.fill(black)
    red_count(r_count)
    blue_count(b_count)

    #drawing on the screen
    for row in grid:
        for node in row:
            pygame.draw.circle(screen, color[node.color], (node.x, node.y), radius)
            pygame.draw.circle(screen, white, (node.x, node.y), radius, 1)
    
    pygame.display.flip()
    # clear_red()
