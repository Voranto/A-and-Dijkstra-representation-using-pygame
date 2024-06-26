import time
import pygame
from sys import exit
import random
from random import choice
import heapq
import math

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
text = my_font.render('Green is Dijkstra', False, (1, 50, 32))
text2 = my_font.render('Blue is A*', False, (0, 0, 255))
grid_size = 20
width = 1400
height = 800
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width+3,height+3))
pygame.display.set_caption("MAZE GENERATION")
class Cell:
    def __init__(self,x,y):
        self.x,self.y = x,y
        self.wall = False
        self.visited = False
        self.path = []
screen.fill("gray")
for i in range(0,width+grid_size,grid_size):
    pygame.draw.line(screen,"black",(i,0),(i,height))
for i in range(0,height+grid_size,grid_size):
    pygame.draw.line(screen,"black",(0,i),(width,i))

arr = [Cell(col,row) for row in range(height//grid_size) for col in range(width//grid_size)]
def check_cell_solve(x,y):
    if x < 0 or x > (width//grid_size) - 1 or y < 0 or y > (height//grid_size) - 1:
        return False
    return arr[x + y * (width//grid_size)]
start = check_cell_solve(0,0)
end = check_cell_solve(width//grid_size-1,height//grid_size-1)
start.path = [start]
start.visited = True
mouse_pressed = False
def bfs():
    stack = [start]
    visited = set([start])
    start.path = [start]
    while stack:  
        curr = stack.pop(0)
        curr.visited = True
        if curr == end:
            break
        x,y = curr.x,curr.y
        for (dx, dy) in (1, 0),(-1, 0), (0, -1), (0, 1),(-1, -1),(-1, 1), (1, -1), (1, 1):
            neighbor = check_cell_solve(x+dx,y+dy)
            if neighbor and neighbor.wall == False and neighbor not in visited and neighbor not in stack:
                if neighbor.path == []:
                    neighbor.path.append(neighbor)
                    for camino in curr.path:
                        neighbor.path.append(camino)
                visited.add(neighbor)
                stack.append(neighbor)
    if curr == end:
        for i in range(1,len(curr.path)):
            pygame.draw.line(screen,"darkgreen",(curr.path[i-1].x*grid_size+grid_size//2,curr.path[i-1].y*grid_size+grid_size//2),(curr.path[i].x*grid_size+grid_size//2,curr.path[i].y*grid_size+grid_size//2),10)
            pygame.draw.circle(screen,"darkgreen",(curr.path[i-1].x*grid_size+grid_size//2,curr.path[i-1].y*grid_size+grid_size//2),3)
        


def astar():
    def h(x,y):
        return math.sqrt((x - end.x)**2 + (y - end.y)**2)
        return abs (x - end.x) + abs (y - end.y)

    def f(h,depth):
        return h*2 + depth
    
    visited_depth = set([(start,0)])
    visited = set([start])
    start.path = [start]
    for i in range((width//grid_size)*(height//grid_size)):
        arr[i].path = []
    g_score = {start:0}
    new_node = start
    start.visited = True
    vecinos_heap = []
    heapq.heappush(vecinos_heap, (f(h(start.x, start.y), 0), 0, (start.x, start.y), start,start))
    while vecinos_heap:
        x, y = new_node.x, new_node.y
        if new_node == end:
            break
        for (dx, dy) in (1, 0),(-1, 0), (0, -1), (0, 1),(-1, -1),(-1, 1), (1, -1), (1, 1):
            neighbor = check_cell_solve(x + dx, y + dy)
            if neighbor and not neighbor.wall and neighbor not in visited :
                tentative_g_score = g_score[new_node] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    heapq.heappush(vecinos_heap, (f(h(x + dx, y + dy), tentative_g_score), tentative_g_score, (x + dx, y + dy), neighbor,new_node))
        # Extraer el vecino con el menor f-score
        _, new_depth, _, new_node,previous = heapq.heappop(vecinos_heap)
        new_node.visited = True
        new_node.path.append(new_node)
        if new_node.path == [new_node]:
            for camino in previous.path:
                if camino not in new_node.path:
                    new_node.path.append(camino)
        visited_depth.add((new_node, new_depth))
        visited.add(new_node)
    if new_node != end:
        print("NO FOUND")
    else:
        for i in range(1,len(new_node.path)):
            pygame.draw.line(screen,"blue",(new_node.path[i-1].x*grid_size+grid_size//2,new_node.path[i-1].y*grid_size+grid_size//2),(new_node.path[i].x*grid_size+grid_size//2,new_node.path[i].y*grid_size+grid_size//2),10)
            #pygame.draw.circle(screen,"blue",(new_node.path[i-1].x*grid_size+grid_size//2,new_node.path[i-1].y*grid_size+grid_size//2),3)
    return 0
impossible = False
squares = set([])
state = "draw"
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pressed = False
            state = "draw"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pressed = True
            state = "draw"
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            mouse_pressed = False
            state = "erase"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_pressed = True
            state = "erase"
        if event.type == pygame.QUIT:
            pygame.QUIT()
            exit()
    screen.fill("gray")
    for i in range(0,width+grid_size,grid_size):
        pygame.draw.line(screen,"black",(i,0),(i,height))
    for i in range(0,height+grid_size,grid_size):
        pygame.draw.line(screen,"black",(0,i),(width,i))
    pygame.draw.rect(screen,"green",(start.x*grid_size,start.y*grid_size,grid_size,grid_size))
    pygame.draw.rect(screen,"red",(end.x*grid_size,end.y*grid_size,grid_size,grid_size))
    if mouse_pressed == True:
        pos = (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        curr = check_cell_solve(pos[0]//grid_size,pos[1]//grid_size)
        if state == "draw":
            if curr:
                squares.add(curr)
                curr.wall = True
                curr.path = []
                curr.visited = False
        else:
            if curr in squares:
                squares.remove(curr)
            curr.wall = False
            curr.path = []
            curr.visited = False
    for square in squares:
        pygame.draw.rect(screen,"black",(square.x *grid_size,square.y*grid_size,grid_size,grid_size))
    impossible_c = astar()
    for i in range((width//grid_size)*(height//grid_size)):
        arr[i].path = []
    bfs()
    screen.blit(text,(width-300,0))
    screen.blit(text2,(width-300,30))
    pygame.display.update()