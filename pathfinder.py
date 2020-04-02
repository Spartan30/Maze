#Import and initialize pygame
import pygame
pygame.init()

import time
import random

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
stack = []
visited = []
solution = {}

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
BLACK = (0,0,0)

def push_up(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y - width + 1, width-1, width*2-1), 0)         # draw a rectangle twice the width of the cell
    pygame.display.update()                                              # to animate the wall being removed


def push_down(x, y):
    pygame.draw.rect(screen, BLUE, (x +  1, y + 1, width-1, width*2-1), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(screen, BLUE, (x - width +1, y +1, width*2-1, width-1), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(screen, BLUE, (x +1, y +1, width*2-1, width-1), 0)
    pygame.display.update()

def single_cell( x, y):
    pygame.draw.rect(screen, GREEN, (x +1, y +1, width - 2, width - 2), 0)          # draw a single width cell
    pygame.display.update()

def backtracking_cell(x, y):
    pygame.draw.rect(screen, BLUE, (x +1, y +1, width - 2, width - 2), 0)        # used to re-colour the path after single_cell
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


def createMaze(x,y):
    stack.append((x,y))
    visited.append((x,y))
    single_cell(x,y)

    while len(stack) > 0:
        time.sleep(.05)
        cell = []

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

                visited.append((x,y))
                stack.append((x,y))
            
            elif neighbour_chosen == "D": #Go down
                push_down(x,y)
                solution[(x, y+width)] = x,y

                y = y + width

                visited.append((x,y))
                stack.append((x,y))

            elif neighbour_chosen == "L": #Go left
                push_left(x,y)
                solution[(x-width,y)] = x,y

                x = x - width

                visited.append((x,y))
                stack.append((x,y))

            elif neighbour_chosen == "U": #Go up
                push_up(x,y)
                solution[(x,y-width)] = x,y

                y = y - width

                visited.append((x,y))
                stack.append((x,y))

        else:
            x, y = stack.pop()                                    # if no cells are available pop one from the stack
            single_cell(x, y)                                     # use single_cell function to show backtracking image
            time.sleep(.05)                                       # slow program down a bit
            backtracking_cell(x, y)                               # change colour to green to identify backtracking path

def plot_route_back(x,y):
    solution_cell(x, y)                                          # solution list contains all the coordinates to route back to start
    while (x, y) != (width,width):                                     # loop until cell position == start position
        x, y = solution[x, y]                                    # "key value" now becomes the new key
        solution_cell(x, y)                                      # animate route back
        time.sleep(.1)


setupGrid(width)
createMaze(width,width)
plot_route_back(screenWidth-width*2, screenHeight-width*2)

#Run until the user asks to quit
running = True
while running:
    #Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#Done
pygame.quit()
