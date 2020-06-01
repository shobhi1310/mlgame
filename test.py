import random

class Node():

    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color

list = []

for i in range(100):
    list.append(Node(random.randint(0,500),random.randint(0,500),random.randint(0,2)))

'''
for i in range(100):
    print('%d %d %d'%(list[i].x,list[i].y,list[i].color))
'''
