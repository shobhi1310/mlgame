import pygame
import random
from collections import Counter
import math
import time

class Node():

    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color

def knn(grid, query_node, k, distance_fn, choice_fn):
    # print(k)
    neighbor_distances_and_indices = []
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if( grid[i][j].x == query_node.x and grid[i][j].y == query_node.y):
                pass
            elif(grid[i][j].color > 1):
                distance = distance_fn(grid[i][j],query_node)
                neighbor_distances_and_indices.append((distance,i,j))

    
    sorted_neighbor_distances_and_indices = sorted(neighbor_distances_and_indices)
    
    k_nearest_distances_and_indices = sorted_neighbor_distances_and_indices[:k]
    
    k_nearest_labels = [grid[i][j].color for distance, i, j in k_nearest_distances_and_indices] 

    return k_nearest_distances_and_indices, choice_fn(k_nearest_labels)

def mean(labels):
    return sum(labels) / len(labels)

def mode(labels):
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

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
start_x = 120
start_y = 120
end = 501
rows = 8
cols = 5
width = 5
height = 5
radius = 20

blue = (0,0,255)
red = (255,0,0)
dull = (69, 79, 70)
white = (255,255,255)
black = (0,0,0)
green = (32, 214, 26)

color=[black,dull,blue,red]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
home_page = pygame.image.load('images/home.png')
instruction_page = pygame.image.load('images/instr.png')
won_page = pygame.image.load('images/won.png')
lost_page = pygame.image.load('images/lost.png')
draw_page = pygame.image.load('images/draw.png')
legion_page = pygame.image.load('images/legion.png')

selector = [(int(20*SCREEN_WIDTH/100), int(SCREEN_HEIGHT/2)),(int(80*SCREEN_WIDTH/100), int(SCREEN_HEIGHT/2))]

running = True
k = -1 # by default k = -1

def red_count(r_count):
    font = pygame.font.SysFont('comicsansms', 40)
    text = font.render("Reds: "+str(r_count), True, red)
    screen.blit(text,(10,0))

def blue_count(b_count):
    font = pygame.font.SysFont('comicsansms', 40)
    text = font.render("Blues: "+str(b_count), True, blue)
    screen.blit(text,(800,0))


class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

#initialising grid
R = 8
r_count = int(R/2)
b_count = int(R/2)
black_count = 2*R
total = rows*cols - black_count
grid = []
def initialize():
    global grid
    global r_count
    global b_count
    global k_nearest_neighbors
    grid = []
    k_nearest_neighbors = []
    y = start_y
    for i in range(rows):
        r = []
        x = start_x
        for j in range(cols):
            r.append(Node(x,y,1))
            x += 2*radius + width
        grid.append(r)
        y += 2*radius + height

    #coloring blue
    for i in range(int(R/2)):
        x = random.randint(0,rows-1)
        y = random.randint(0,cols-1)
        grid[x][y].color = 2

    #coloring red
    for i in range(int(R/2)):
        check = True
        while(check):
            x = random.randint(0,rows-1)
            y = random.randint(0,cols-1)
            if grid[x][y].color == 2:
                x = random.randint(0,rows-1)
                y = random.randint(0,cols-1)
            else:
                grid[x][y].color = 3
                check = False

    #coloring black
    for i in range(black_count):
        check = True
        while(check):
            x = random.randint(0,rows-1)
            y = random.randint(0,cols-1)
            if grid[x][y].color == 2 or grid[x][y].color == 3:
                x = random.randint(0,rows-1)
                y = random.randint(0,cols-1)
            else:
                grid[x][y].color = 0
                check = False
    
    # re-initialise            
    r_count = int(R/2)
    b_count = int(R/2)

start = button(green,int(10*SCREEN_WIDTH/100),SCREEN_HEIGHT-60,100,40,'Start')
instr = button(green,int(40*SCREEN_WIDTH/100),SCREEN_HEIGHT-60,230,40,'Instruction')
reMatch = button(green,int(SCREEN_WIDTH/2),SCREEN_HEIGHT-60,200,40,'Rematch')
proceed = button(green,int(10*SCREEN_WIDTH/100),SCREEN_HEIGHT/2,130,40,'Proceed')

#Game state
state = 0

def home():
    global running
    global state
    screen.blit(home_page,(0,0))
    start.draw(screen,red)
    instr.draw(screen,red)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start.isOver(pygame.mouse.get_pos()):
                state = 2
            elif instr.isOver(pygame.mouse.get_pos()):
                state = 1

def instruct():
    global running
    global state
    screen.blit(instruction_page,(0,0))
    start.draw(screen,red)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start.isOver(pygame.mouse.get_pos()):
                state = 2

def choose_k():
    global running
    global state
    global k
    font = pygame.font.SysFont(None, 25)
    text = font.render('Choose K to be a odd integer from 3 to 9 then press ENTER. or BACKSPACE to delete', True, red)
    screen.blit(text,(int(20*SCREEN_WIDTH/100),SCREEN_HEIGHT/2))

    font_k = pygame.font.SysFont(None, 25)
    text_k = font.render('Chosen K : ', True, red)
    screen.blit(text_k,(int(20*SCREEN_WIDTH/100),SCREEN_HEIGHT/2+50))

    font_hint = pygame.font.SysFont(None, 25)
    if k!=-1:
        text_hint = font.render(str(k), True, red)
        screen.blit(text_hint,(int(20*SCREEN_WIDTH/100 + 100),SCREEN_HEIGHT/2+50))
    pygame.display.flip()
    # proceed.draw(screen,red)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    state = 3
                elif event.key == pygame.K_BACKSPACE:
                    k = -1
                else:
                    k = int(event.key) - 48


selected = 0 #by default blue.
def choose_side():
    global running
    global state
    global selected
    screen.blit(legion_page,(0,0))
    # blue
    pygame.draw.circle(screen, color[2], selector[0], radius)
    pygame.draw.circle(screen, white, selector[0], radius, 1)

    # red
    pygame.draw.circle(screen, color[3], selector[1], radius)
    pygame.draw.circle(screen, white, selector[1], radius, 1)

    # proceed.draw(screen,red)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if screen.get_at(pygame.mouse.get_pos()) == red:
                selected = 1
            state = 4

k_nearest_neighbors = []
def game():
    global r_count
    global b_count
    global running
    global state
    global k_nearest_neighbors
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            X = pygame.mouse.get_pos()[0]
            Y = pygame.mouse.get_pos()[1]
            for i in range(rows):
                for j in range(cols):
                    if((X-grid[i][j].x)**2 + (Y-grid[i][j].y)**2 - radius**2) <= 0:
                        if grid[i][j].color == 1:
                            k_nearest_neighbors, grid[i][j].color = knn(grid,grid[i][j],k,distance_fn=euclidean_distance, choice_fn=mode)
                            # highlight(grid,k_nearest_neighbors)
                            if(grid[i][j].color == 2):
                                b_count += 1
                            else:
                                r_count += 1
                            break
    #score display
    red_count(r_count)
    blue_count(b_count)

    #state changer
    if r_count + b_count == total:
        print(total)
        state = 5

    #drawing on the screen
    for row in grid:
        for node in row:
            pygame.draw.circle(screen, color[node.color], (node.x, node.y), radius)
            if node.color != 0:
                pygame.draw.circle(screen, white, (node.x, node.y), radius, 1)
    
    if len(k_nearest_neighbors) != 0:
        for distance, i, j in k_nearest_neighbors:
            pygame.draw.circle(screen, (210, 235, 52), (grid[i][j].x, grid[i][j].y), radius, 4)
        
        # time.sleep(0.2)
        
        for distance, i, j in k_nearest_neighbors:
            pygame.draw.circle(screen, white, (grid[i][j].x, grid[i][j].y), radius, 1)


def end_screen():
    global running
    global state
    if(selected==0):    # player is blue
        if(b_count>r_count):
            screen.blit(won_page,(0,0))
        elif(b_count==r_count):
            screen.blit(draw_page,(0,0))
        else:
            screen.blit(lost_page,(0,0))
    else:
        if(b_count<r_count):
            screen.blit(won_page,(0,0))
        elif(b_count==r_count):
            screen.blit(draw_page,(0,0))
        else:
            screen.blit(lost_page,(0,0))

    reMatch.draw(screen,red)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if reMatch.isOver(pygame.mouse.get_pos()):
                initialize()
                state = 4

# Main loop
initialize()
while running:
    screen.fill(black)
    if state == 0:
        home()
    elif state == 1:
        instruct()
    elif state == 2:
        choose_k()
    elif state == 3:
        choose_side()
    elif state == 4:
        game()
    elif state == 5:
        end_screen()
    pygame.display.flip()
