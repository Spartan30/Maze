#Import and initialize pygame
import pygame
pygame.init()

import time
import random
import math
from node import node

screenWidth = 600
screenHeight = 600

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
solution = {}

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
BLACK = (0,0,0)
RED = (255,0,0)
PURPLE = (255,0,255)

def push_up(x, y):
    pygame.draw.rect(screen, WHITE, (x + 1, y - width + 1, width-1, width*2-1), 0)         # draw a rectangle twice the width of the cell
    pygame.display.update()                                              # to animate the wall being removed


def push_down(x, y):
    pygame.draw.rect(screen, WHITE, (x +  1, y + 1, width-1, width*2-1), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(screen, WHITE, (x - width +1, y +1, width*2-1, width-1), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(screen, WHITE, (x +1, y +1, width*2-1, width-1), 0)
    pygame.display.update()

def single_cell( x, y):
    pygame.draw.rect(screen, GREEN, (x +1, y +1, width - 1, width - 1), 0)          # draw a single width cell
    pygame.display.update()

def backtracking_cell(x, y):
    pygame.draw.rect(screen, WHITE, (x +1, y +1, width - 1, width - 1), 0)        # used to re-colour the path after single_cell
    pygame.display.update()                                        # has visited cell

def solution_cell(x,y):
    pygame.draw.rect(screen, YELLOW, (x+8, y+8, 5, 5), 0)             # used to show the solution
    pygame.display.update()                                        # has visited cell

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

#Create the Maze
def createMaze(x,y):
    stack.append((x,y))
    visited.append((x,y))
    single_cell(x,y)

    while len(stack) > 0:
        time.sleep(.02)
        cell = []

        neighbourNode = None
        currNode = findNode(x,y)

        #Search for unvisited neighbours
        if (x+width, y) not in visited and (x+width, y) in grid: #Check cell to right
            cell.append("R")
        
        if (x, y+width) not in visited and (x, y+width) in grid: #Check cell to bottom
            cell.append("D")
        
        if (x-width, y) not in visited and (x-width, y) in grid: #Check cell to left
            cell.append("L")
        
        if (x, y-width) not in visited and (x, y-width) in grid: #Check cell to top
            cell.append("U")


        #Check if there is available neighbour
        if len(cell) > 0:
            neighbour_chosen = (random.choice(cell))

            if neighbour_chosen == 'R': #Go right
                push_right(x,y)
                solution[(x+width, y)] = x,y

                x = x + width

                currNode.neighbours.append((x,y))

                neighbourNode = findNode(x,y)
                neighbourNode.neighbours.append((currNode.x, currNode.y))

                visited.append((x,y))
                stack.append((x,y))
            
            elif neighbour_chosen == "D": #Go down
                push_down(x,y)
                solution[(x, y+width)] = x,y

                y = y + width

                currNode.neighbours.append((x,y))

                neighbourNode = findNode(x,y)
                neighbourNode.neighbours.append((currNode.x, currNode.y))

                visited.append((x,y))
                stack.append((x,y))

            elif neighbour_chosen == "L": #Go left
                push_left(x,y)
                solution[(x-width,y)] = x,y

                x = x - width

                currNode.neighbours.append((x,y))

                neighbourNode = findNode(x,y)
                neighbourNode.neighbours.append((currNode.x, currNode.y))

                visited.append((x,y))
                stack.append((x,y))

            elif neighbour_chosen == "U": #Go up
                push_up(x,y)
                solution[(x,y-width)] = x,y

                y = y - width

                currNode.neighbours.append((x,y))

                neighbourNode = findNode(x,y)
                neighbourNode.neighbours.append((currNode.x, currNode.y))

                visited.append((x,y))
                stack.append((x,y))

        else:
            x, y = stack.pop()                                    # if no cells are available pop one from the stack
            single_cell(x, y)                                     # use single_cell function to show backtracking image
            time.sleep(.02)                                       # slow program down a bit
            backtracking_cell(x, y)                               # change colour to green to identify backtracking path

#Obsolete
def plot_route_back(x,y):
    solution_cell(x, y)                                          # solution list contains all the coordinates to route back to start
    while (x, y) != (width,width):                                     # loop until cell position == start position
        x, y = solution[x, y]                                    # "key value" now becomes the new key
        solution_cell(x, y)                                      # animate route back
        time.sleep(.1)

#Create a start or end node
def createNode(x,y,width):
    newNode = node()
    newNode.x = x
    newNode.y = y
    newNode.neighbours = []

    return newNode

#Create a code and append it to 'nodes'
def setNode(x,y,width):
    newNode = node()
    newNode.x = x
    newNode.y = y
    newNode.neighbours = []
    
    #Calculate g and h
    newNode.g = int(abs(x-startNode.x)/width) + int(abs(y-startNode.y)/width)
    newNode.h = int(abs(x-endNode.x)/width)**2 + int(abs(y-endNode.y)/width)**2

    #Calculate f
    newNode.f = int(newNode.g + newNode.h)

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
    return None

#Find the path between start and end node
#F total cost
#G cost to start
#H cost to end
def findPath(x,y,width):

    #Clear lists
    openSet.clear()
    closeSet.clear()
    visited.clear()
    stack.clear()

    #Add start node to openSet
    openSet.append(findNode(x,y))

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
                    checkNode.f = checkNode.g + checkNode.h
                    checkNode.parent = currNode
                    continue

            #Node is not in openSet or closeSet, update g and f
            checkNode.g = currNode.g + 1
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


#Setup grid
setupGrid(width)

#Set default start node
startNode = createNode(width, width, width)
startNode.f = 0
startNode.g = 0

#Set default end node
endNode = createNode(screenWidth-width*2, screenHeight-width*2, width)
endNode.f = 0
endNode.h = 0

#Get all the nodes
setupNodes(width)

#Create maze
createMaze(width,width)


#Show start and end nodes
pygame.draw.rect(screen, GREEN, (startNode.x+1, startNode.y+1, width-1, width-1),0)   
pygame.draw.rect(screen, RED, (endNode.x+1, endNode.y+1, width-1, width-1),0)

#Draw start button
pygame.draw.rect(screen,GREEN,(0,0,30,20),0)

#Draw restart button
pygame.draw.rect(screen, RED, (50,0,30,20),0)

pygame.display.flip()

#plot_route_back(screenWidth-width*2, screenHeight-width*2)

#Run until the user asks to quit
running = True
while running:
    #Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Mouse click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #Left click, get position
                pos = pygame.mouse.get_pos()

                    #Node was not clicked
                if pos[0] > 0 and pos[0] < 30 and pos[1] > 0 and pos[1] < 20:
                    #Start button was clicked
                    #Find path
                    path = findPath(startNode.x, startNode.y, width)

                    if path is not None:

                        #Draw path starting at beginning
                        for p in path:
                            pygame.draw.rect(screen, GREEN, (p.x+1, p.y+1, width-1, width-1),0)
                            pygame.display.update()   
                            time.sleep(.01)

                    #Font
                    default_font = pygame.font.get_default_font()
                    font_renderer = pygame.font.Font(default_font, 12)

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
                    setupNodes(width)

                    #Creat Maze
                    createMaze(width,width)

                    pygame.draw.rect(screen, GREEN, (startNode.x+1, startNode.y+1, width-1, width-1),0)

                    pygame.draw.rect(screen, RED, (endNode.x+1, endNode.y+1, width-1, width-1),0)


                    #Draw start button
                    pygame.draw.rect(screen,GREEN,(0,0,30,20),0)

                    #Draw end button
                    pygame.draw.rect(screen, RED, (50,0,30,20),0)


                    #Flip the display
                    pygame.display.flip()


#Done
pygame.quit()
