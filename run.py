#Import and initialize pygame
import pygame
pygame.init()

import threading
import time
import random
import math
from node import node

#Screen size
screenWidth = 400
screenHeight = 400

#Set up drawing window
screen = pygame.display.set_mode([screenWidth, screenHeight])

#Variables
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
RED = (255,0,0)
PURPLE = (255,0,255)

#Create the grid
def setupGrid(width):

    #Fill the background with white
    screen.fill((255,255,255))

    grid.clear()

    for y in range(width, (screenHeight-width), width):
        for x in range(width, (screenWidth-width), width):
            pygame.draw.line(screen, BLACK, [x, y], [x + width, y])           # top of cell
            pygame.draw.line(screen, BLACK, [x + width, y], [x + width, y + width])   # right of cell
            pygame.draw.line(screen, BLACK, [x + width, y + width], [x, y + width])   # bottom of cell
            pygame.draw.line(screen, BLACK, [x, y + width], [x, y])           # left of cell
            grid.append((x,y))


    #Flip the display
    pygame.display.flip()

#Create a start or end node
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

#Create a code and append it to 'nodes'
def setNode(x,y,width):
    newNode = node()
    newNode.x = x
    newNode.y = y
    newNode.neighbours = []
    
    newNode.g = 0
    newNode.h = 0
    newNode.f = 0

    #Calculate g and h
    #newNode.g = int(abs(x-startNode.x)/width) + int(abs(y-startNode.y)/width)
    #newNode.h = int(abs(x-endNode.x)/width)**2 + int(abs(y-endNode.y)/width)**2

    #Calculate f
    #newNode.f = int(newNode.g + newNode.h)

    #Find neighbours
    if (x+width, y) in grid: #Check Right
        newNode.neighbours.append((x+width,y))

    if (x, y + width) in grid: #Check Down
        newNode.neighbours.append((x,y+width))

    if(x-width,y) in grid: #Check Left
        newNode.neighbours.append((x-width,y))
    
    if(x, y-width) in grid: #Check up
        newNode.neighbours.append((x, y-width))

    nodes.append(newNode)

#Setup all nodes
def setupNodes(width):
    nodes.clear()
    for x,y in grid:
        setNode(x,y,width)

#Find a node in the 'nodes' list
def findNode(x,y):
    for n in nodes:
        if n.x == x and n.y ==y:
            return n

#Find the path between start and end node
#F total cost
#G cost to start
#H cost to end
def findPath(x,y,width,endNode):

    #Clear lists
    openSet.clear()
    closeSet.clear()
    visited.clear()
    stack.clear()

    firstNode = findNode(x,y)
    firstNode.g = 0
    firstNode.h = 0
    firstNode.f = 0

    #Add start node to openSet
    openSet.append(firstNode)

    #While openSet is not empty
    while len(openSet) > 0:
        currNode = None
        checkNode = None
        minF = 99999999999999999
        minH = 99999999999999999
        minG = 99999999999999999

        #Find best node in openSet
        for n in openSet:
            #Check status of node's f vs minF
            if n.f == minF:
                #Node's f is equal to minF, use H as tie breaker
                if n.h < minH:
                    minH = n.h
                    minF = n.f
                    minG = n.g
                    currNode = n

            elif n.f < minF:
                #Node's f is less than minF
                minF = n.f
                minH = n.h
                minG = n.g
                currNode = n
                
        #Remove current node from openSet and add to closeSet
        openSet.remove(currNode)
        closeSet.append(currNode)

        #Draw current square being checked
        pygame.draw.rect(screen, PURPLE, (currNode.x+1, currNode.y+1, width-1, width-1),0)
        pygame.display.update()   
        time.sleep(.02)

        #Check if end has been reached
        if currNode.x == endNode.x and currNode.y == endNode.y:
            #Found end
            print("FOUND: ",endNode.x,endNode.y)
            path = []

            #Keep looping until start is reached
            while currNode is not None:
                #Add node to path
                path.append(currNode)

                #Set node to be parent node
                currNode = currNode.parent

            #Return the path in reverse
            return path[::-1]
            

        for x,y in currNode.neighbours:
            #Get neighbour node
            checkNode = findNode(x,y)

            if checkNode in closeSet:
                #Node is already in closed set
                #Check if path from start through currNode is shorter than through the closedNode's parent
                if(currNode.g+1) < checkNode.g:
                    #Path is shorter, change parent to currNode and update g and f
                    checkNode.parent = currNode
                    checkNode.g = currNode.g+1
                    checkNode.h = int(abs(x-endNode.x)/width)**2 + int(abs(y-endNode.y)/width)**2
                    checkNode.f = checkNode.g + checkNode.h 
                continue
            
            #Check if node is passable
            if checkNode.passable != 0:
                #Node is not passable
                continue


            if checkNode in openSet:
                #checkNode is already in openSet
                #Check if the new g value for checkNode will be higher than its current g value
                if (currNode.g + 1) > checkNode.g:
                    #New g value is higher than current g value, keep current value
                    continue
                else:
                    #Check node is in openSet and new g value is less then or equal to current g value
                    #Update g and f value
                    checkNode.g = currNode.g + 1
                    checkNode.h = int(abs(x-endNode.x)/width)**2 + int(abs(y-endNode.y)/width)**2
                    checkNode.f = checkNode.g + checkNode.h
                    checkNode.parent = currNode
                    continue

            #Node is not in openSet or closeSet, update g and f
            checkNode.g = currNode.g + 1
            checkNode.h = int(abs(x-endNode.x)/width)**2 + int(abs(y-endNode.y)/width)**2
            checkNode.f = checkNode.g + checkNode.h

            #Draw openSet square
            pygame.draw.rect(screen, BLUE, (checkNode.x+1, checkNode.y+1, width-1, width-1),0)
            pygame.display.update()   
            time.sleep(.02)

            #Set nodes parent and add to openSet
            checkNode.parent = currNode
            openSet.append(checkNode)

        #Draw closeSet square
        pygame.draw.rect(screen, YELLOW, (currNode.x+1, currNode.y+1, width-1, width-1),0)
        pygame.display.update()   
        time.sleep(.02)

    #No path found
    print("No Path Found!")

    #Set all closeSet square to red
    for n in closeSet:
        pygame.draw.rect(screen, RED, (n.x+1, n.y+1, width-1, width-1),0)
        pygame.display.update()   

    #Return None
    return None


#Setup the grid
setupGrid(width)

#Set default start node
enemyNode = createNode(screenWidth-width*2, screenHeight-width*2, width)
enemyNode.f = 0
enemyNode.g = 0
pygame.draw.rect(screen, RED, (enemyNode.x+1, enemyNode.y+1, width-1, width-1),0)   

#Set default end node
playerNode = createNode(width, width, width)
playerNode.f = 0
playerNode.h = 0
pygame.draw.rect(screen, GREEN, (playerNode.x+1, playerNode.y+1, width-1, width-1),0)


#Get all the nodes
setupNodes(width)

#Draw start button
pygame.draw.rect(screen,GREEN,(0,0,30,20),0)

#Draw restart button
pygame.draw.rect(screen, RED, (50,0,30,20),0)

#Flip the display
pygame.display.flip()

#Run until the user asks to quit
running = True
while running:
    #Did the user click the window close button?
    for event in pygame.event.get():
        #Check event type
        if event.type == pygame.QUIT:
            #Quit game
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if (playerNode.x,playerNode.y-width) in grid:
                    #Move up
                    pygame.draw.rect(screen, WHITE, (playerNode.x+1, playerNode.y+1, width-1, width-1),0)

                    playerNode.y -= width

                    pygame.draw.rect(screen, GREEN, (playerNode.x+1, playerNode.y+1, width-1, width-1),0)
                    pygame.display.flip()

            elif event.key == pygame.K_a:
                if (playerNode.x-width,playerNode.y) in grid:
                    #Move left
                    pygame.draw.rect(screen, WHITE, (playerNode.x+1, playerNode.y+1, width-1, width-1),0)

                    playerNode.x -= width

                    pygame.draw.rect(screen, GREEN, (playerNode.x+1, playerNode.y+1, width-1, width-1),0)
                    pygame.display.flip()

            elif event.key == pygame.K_s:
                if (playerNode.x,playerNode.y+width) in grid:
                    #Move down
                    pygame.draw.rect(screen, WHITE, (playerNode.x+1, playerNode.y+1, width-1, width-1),0)

                    playerNode.y += width

                    pygame.draw.rect(screen, GREEN, (playerNode.x+1, playerNode.y+1, width-1, width-1),0)
                    pygame.display.flip()

            elif event.key == pygame.K_d:
                if (playerNode.x+width,playerNode.y) in grid:
                    #Move right
                    pygame.draw.rect(screen, WHITE, (playerNode.x+1, playerNode.y+1, width-1, width-1),0)

                    playerNode.x += width

                    pygame.draw.rect(screen, GREEN, (playerNode.x+1, playerNode.y+1, width-1, width-1),0)
                    pygame.display.flip()
        
        #Mouse click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #Left click, get position
                pos = pygame.mouse.get_pos()

                #Find node that was clicked on
                clickNode = findNode(int(pos[0]/width)*width, int(pos[1]/width)*width)

                #Check if a node was clicked
                if clickNode is not None:
                    #Node was clicked
                    if clickNode.passable == 0:
                        #Node is passable, set to not passable
                        clickNode.passable = 1
                        pygame.draw.rect(screen, BLACK, (clickNode.x+1, clickNode.y+1, width-1, width-1),0)
                        pygame.display.update()  
                    else:
                        #Not is not passable, set to passable
                        clickNode.passable = 0 
                        pygame.draw.rect(screen, WHITE, (clickNode.x+1, clickNode.y+1, width-1, width-1),0)
                        pygame.display.update()  
                
                else:
                    #Node was not clicked
                    if pos[0] > 0 and pos[0] < 30 and pos[1] > 0 and pos[1] < 20:
                        #Start button was clicked
                        #Find path
                        path = findPath(enemyNode.x, enemyNode.y, width, playerNode)

                        if path is not None:

                            #Draw path starting at beginning
                            for p in path:
                                pygame.draw.rect(screen, GREEN, (p.x+1, p.y+1, width-1, width-1),0)
                                pygame.display.update()   
                                time.sleep(.01)

                        #Font
                        #default_font = pygame.font.get_default_font()
                        #font_renderer = pygame.font.Font(default_font, 12)

                        #Display f's
                        #for n in nodes:
                            #label = font_renderer.render(str(int(n.f)),1,(0,0,0))
                            #screen.blit(label,(n.x,n.y))
                            #label = font_renderer.render(str(int(n.g)),1,(0,0,0))
                            #screen.blit(label,(n.x,n.y+13))

                        #Flip the display
                        pygame.display.flip()

                    elif pos[0] > 50 and pos[0] < 80 and pos[1] > 0 and pos[1] < 20:
                        #Restart button was clicked
                        print("Restart")

                        #Setup the grid
                        setupGrid(width)

                        #Get all the nodes
                        #setupNodes(width)

                        pygame.draw.rect(screen, GREEN, (playerNode.x+1, playerNode.y+1, width-1, width-1),0)

                        pygame.draw.rect(screen, RED, (enemyNode.x+1, enemyNode.y+1, width-1, width-1),0)


                        #Draw start button
                        pygame.draw.rect(screen,GREEN,(0,0,30,20),0)

                        #Draw end button
                        pygame.draw.rect(screen, RED, (50,0,30,20),0)


                        #Flip the display
                        pygame.display.flip()

#Done
pygame.quit()
