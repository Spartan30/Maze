#Import and initialize pygame
import pygame
pygame.init()

import time
import random
import math
from node import node

screenWidth = 400
screenHeight = 400

#Set up drawing window
screen = pygame.display.set_mode([screenWidth, screenHeight])

width = 25
lineWidth = 0
colour = 0
xTiles = int(screenWidth/width)
yTiles = int(screenHeight/width)
grid = []
nodes = []
openSet = []
closeSet = []
stack = []
visited = []

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
BLACK = (0,0,0)



def setupGrid(width):

    #Fill the background with white
    screen.fill((255,255,255))

    for y in range(width, (screenHeight-width), width):
        for x in range(width, (screenWidth-width), width):
            pygame.draw.line(screen, BLACK, [x, y], [x + width, y])           # top of cell
            pygame.draw.line(screen, BLACK, [x + width, y], [x + width, y + width])   # right of cell
            pygame.draw.line(screen, BLACK, [x + width, y + width], [x, y + width])   # bottom of cell
            pygame.draw.line(screen, BLACK, [x, y + width], [x, y])           # left of cell
            grid.append((x,y))


    #Flip the display
    pygame.display.flip()

def createNode(x,y,width):
    newNode = node()
    newNode.x = x
    newNode.y = y
    newNode.neighbours = []

    if (x+width, y) in grid: #Check Right
        newNode.neighbours.append((x+width,y))

    if (x, y + width) in grid: #Check Down
        newNode.neighbours.append((x,y+width))

    if(x-width,y) in grid: #Check Left
        newNode.neighbours.append((x-width,y))
    
    if(x, y-width) in grid: #Check up
        newNode.neighbours.append((x, y-width))

    return newNode

def setNode(x,y,width):
    newNode = node()
    newNode.x = x
    newNode.y = y
    newNode.neighbours = []
    
    newNode.g = math.sqrt((x-startNode.x)**2 + (y-startNode.y)**2)
    newNode.h = math.sqrt((x-endNode.x)**2 + (y-endNode.y)**2)

    newNode.f = newNode.g + newNode.h

    if (x+width, y) in grid: #Check Right
        newNode.neighbours.append((x+width,y))

    if (x, y + width) in grid: #Check Down
        newNode.neighbours.append((x,y+width))

    if(x-width,y) in grid: #Check Left
        newNode.neighbours.append((x-width,y))
    
    if(x, y-width) in grid: #Check up
        newNode.neighbours.append((x, y-width))

    nodes.append(newNode)


def setupNodes(width):
    for x,y in grid:
        setNode(x,y,width)

def findNode(x,y):
    for n in nodes:
        if n.x == x and n.y ==y:
            return n

#F total cost
#G cost to start
#H cost to end
def findPath(width):
    openSet.append(startNode)

    while len(openSet) > 0:
        currNode = None
        checkNode = None
        minF = 99999999999999999

        for n in openSet:
            if n.f < minF:
                minF = n.f
                currNode = n
                
        openSet.remove(currNode)
        closeSet.append(currNode)

        pygame.draw.rect(screen, BLUE, (currNode.x, currNode.y, width, width),0)
        pygame.display.update()   

        if currNode.x == endNode.x and currNode.y == endNode.y:
            print("FOUND: ",endNode.x,endNode.y)
            return
            

        for x,y in currNode.neighbours:
            checkNode = findNode(x,y)

            if checkNode in closeSet:
                continue

            if checkNode in openSet:
                continue
            
            openSet.append(checkNode)
        

#Setup the grid
setupGrid(width)

#Get start and end nodes
startNode = createNode(width, width, width)
startNode.f = 0

endNode = createNode(screenWidth-width*2, screenHeight-width*2, width)

#Get all the nodes
setupNodes(width)

findPath(width)

default_font = pygame.font.get_default_font()
font_renderer = pygame.font.Font(default_font, 12)

#Display f's
#for n in nodes:
#    label = font_renderer.render(str(int(n.f)),1,(0,0,0))
#    screen.blit(label,(n.x,n.y))

#Flip the display
#pygame.display.flip()

#Run until the user asks to quit
running = True
while running:
    #Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#Done
pygame.quit()
