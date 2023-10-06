import curses
from curses import wrapper
import queue
import time 



# Maze design - 0 starting poin , X ending point , # - obstacles  
maze = [
    ["#", "#", "#", "#", "#", "#", "O", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def display_maze(maze,stdscr,path=[]):
    
    CYAN = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze): # get index and value from enumerate / row = list
        for j , val in enumerate(row): # j = column / val = symbol in the column
            if (i,j) in path:
                stdscr.addstr(i,j*2,"X",RED)
            else:
                stdscr.addstr(i,j*2,val,CYAN)


# to get the starting position
def find_start(maze,startSymbl):
    for i, row in enumerate(maze):
        for j , value in enumerate(row):
            if value == startSymbl:
                return i, j

    return None

# BFS algorithm (Breadth-first-search)
def find_path(maze,stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze,start)

    # FIFO queue
    q = queue.Queue()
    q.put((start_pos,[start_pos]))

    visited = set()

    while not q.empty():
        # get what next in queue
        current_pos, path = q.get() 
        row , col = current_pos

        stdscr.clear() # clear entire screen
        display_maze(maze,stdscr, path)
        # to visualize what happens
        time.sleep(0.2)
        stdscr.refresh() # refresh screen 


        # if the shortest path is found return the path
        if maze [row][col] == end:
            return path
        
        neighbors = find_neighbors(maze,row,col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            r, c = neighbor
            if maze[r][c] == "#":
                continue
            
            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)



def find_neighbors(maze,row,col):
    neighbors = []

    if row > 0 : # UP
        neighbors.append((row-1,col))
    if row +1 < len(maze): # DOWN
        neighbors.append((row+1 , col))
    if col > 0 : # LEFT
        neighbors.append((row,col-1))
    if col +1 < len(maze[0]) : # RIGHT
        neighbors.append((row,col+1))

    return neighbors



def main (stdscr):
    # add colors
    curses.init_pair(1,curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_RED, curses.COLOR_BLACK)
    find_path(maze,stdscr)
    stdscr.getch() # wait until user hit something before exiting

# initialize the curses module, call the function and pass the stdscr object to control output
wrapper(main) 
