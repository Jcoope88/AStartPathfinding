import pygame, math
from queue import PriorityQueue


#INIT
width = 800
win = pygame.display.set_mode((width,width))
pygame.display.set_caption("Astar Pathfinding")

#COLORS 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot: 
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self): 
        return self.color == PRUPLE

    def is_open(self):
        return self.color == BLUE

    def is_collider(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == GREEN

    def is_end(self):
        return self.color == RED


    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = PURPLE

    def make_open(self):
        self.color = BLUE

    def make_collider(self):
        self.color = BLACK

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = RED 

    def make_path(self):
        self.color = ORANGE

    def draw(self, win):
        pygame.draw.rect(win,self.color,(self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_collider(): #down check
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_collider(): #up check
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_collider(): #right check
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_collider(): #left check
            self.neighbors.append(grid[self.row][self.col - 1])



    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current  in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue() #efficient way to min element
    open_set.put((0, count, start))
    came_from = {}
    
    #end to start
    g_score = {spot: float("inf") for row in grid for spot in row} 
    g_score[start] = 0

    #current pos to end
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start} #check whats inside priorityqueue

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2] #set node
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def make_grid(rows, width): #rows and collumn same
    grid = []
    gap = width // rows #integar division, what should the width of the cubes be
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def  draw_grid(win, rows, width): #draw grid lines
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) #row lines, horizontal
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width)) #collumn lines, vertical
        
def draw(win, grid, rows, width):
    win.fill(WHITE) #re-draw

    for row in grid: #draw all the 'colors'
        for spot in row: 
            spot.draw(win)

    draw_grid(win, rows, width) #draw lines ontop of 'colors'
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    
    row = y // gap 
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    
    start = None
    end = None

    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get(): #get events
            # pylint: disable=no-member
            if event.type == pygame.QUIT:
            # pylint: enable=no-member
                run = False

            if pygame.mouse.get_pressed()[0]: #left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()
                
                elif spot != end and spot != start:
                    spot.make_collider()

            elif pygame.mouse.get_pressed()[2]: #right mouse button    
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    # pylint: disable=no-member
    pygame.quit()
    # pylint: enable=no-member

main(win, width)