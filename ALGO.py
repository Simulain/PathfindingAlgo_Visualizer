from queue import PriorityQueue
from collections import deque
from NODE import *
import random
import time

### PATHFINDING ALGORITHMS

# f(x) = g(x)
def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}  # Distance from start
    g_score[start] = 0

    open_set_h = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_h.remove(current)

        if current == end:
            make_path(came_from, end, draw)
            return True

        for adjacent in current.adjacent:
            temp_g_score = g_score[current] + 1 # All squares are equal value (1)

            if temp_g_score < g_score[adjacent]:
                came_from[adjacent] = current
                g_score[adjacent] = temp_g_score

                if adjacent not in open_set_h:
                    count += 1
                    open_set.put((g_score[adjacent], count, adjacent))
                    open_set_h.add(adjacent)
                    if adjacent != end:
                        adjacent.set_open()

        draw()

        if current != start:
            current.set_closed()

    return False

# f(x) = g(x) + h(x)
def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}  # Distance from start
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}  # Combined distance from start and end
    f_score[start] = euclidean_dist(start.get_pos(), end.get_pos())

    open_set_h = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_h.remove(current)

        if current == end:
            make_path(came_from, end, draw)
            return True

        for adjacent in current.adjacent:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[adjacent]:
                came_from[adjacent] = current
                g_score[adjacent] = temp_g_score
                f_score[adjacent] = temp_g_score + euclidean_dist(adjacent.get_pos(), end.get_pos())

                if adjacent not in open_set_h:
                    count += 1
                    open_set.put((f_score[adjacent], count, adjacent))
                    open_set_h.add(adjacent)
                    if adjacent != end:
                        adjacent.set_open()

        draw()

        if current != start:
            current.set_closed()

    return False

# f(x) = h(x)
def greedy_best_first(draw, grid, start, end):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}  # Used to make the final path
    g_score[start] = 0
    h_score = {node: float("inf") for row in grid for node in row}
    h_score[start] = euclidean_dist(start.get_pos(), end.get_pos())

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]

        if current == end:
            make_path(came_from, end, draw)
            return True

        for adjacent in current.adjacent:
            temp_g_score = g_score[current] + 1

            if not adjacent.is_visited():
                if temp_g_score < g_score[adjacent]:
                    came_from[adjacent] = current
                    g_score[adjacent] = temp_g_score

                adjacent.set_visited()
                h_score[adjacent] = euclidean_dist(adjacent.get_pos(), end.get_pos())
                open_set.put((h_score[adjacent], adjacent))
                if adjacent not in (start, end):
                    adjacent.set_open()

        draw()

        if current != start:
            current.set_closed()

    return False

def depth_first(draw, grid, start, end):
    open_set = deque([start])
    came_from = {}

    while (len(open_set) != 0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.pop()

        if current == end:
            make_path(came_from, end, draw)
            return True

        if current.is_visited():
            current.set_open()
            draw()
            time.sleep(0.01)

        current.set_visited()


        for adjacent in current.adjacent:
            if not adjacent.is_visited() and not adjacent.is_wall():
                open_set.append(adjacent)
                came_from[adjacent] = current
                if adjacent not in (start, end):
                    adjacent.set_open()

        draw()

        if current != start:
            current.set_closed()

    return False

def breadth_first(draw, grid, start, end):
    open_set = deque([start])
    came_from = {}

    while (len(open_set) != 0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.pop()

        if current == end:
            make_path(came_from, end, draw)
            return True

        for adjacent in current.adjacent:
            if not adjacent.is_visited() and not adjacent.is_wall() and adjacent not in open_set:
                open_set.appendleft(adjacent)
                current.set_visited()
                came_from[adjacent] = current
                if adjacent not in (start, end):
                    adjacent.set_open()

        draw()

        if current != start:
            current.set_closed()

    return False


### MAZE GENERATING ALGORITHMS

def make_maze(draw, grid):
    wall_edges(draw, grid)

    VERTICAL = 0
    HORIZONTAL = 1

    stack = [((1, 1), (BOARD_SIZE_Y - 2, BOARD_SIZE_X - 2))]

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop(-1)
        min_y = current[0][0]
        max_y = current[1][0]
        min_x = current[0][1]
        max_x = current[1][1]
        height = max_y - min_y + 1
        width = max_x - min_x + 1

        time.sleep(0.01)

        if height <= 1 or width <= 1:
            continue

        if width < height:
            cut_direction = HORIZONTAL
        elif width > height:
            cut_direction = VERTICAL
        else:
            if width == 2:
                continue
            cut_direction = random.randrange(2)

        if cut_direction is VERTICAL:
            cut_length = width
        else:
            cut_length = height
        if cut_length < 3:
            continue

        cut_position = random.randrange(1, cut_length, 2)
        gap_position = random.randrange(0, (height, width)[cut_direction], 2)

        if cut_direction is VERTICAL:
            for row in range(min_y, max_y + 1):
                grid[row][min_x + cut_position].set_wall()
                draw()
            grid[min_y + gap_position][min_x + cut_position].reset()
            draw()
        else:
            for col in range(min_x, max_x + 1):
                grid[min_y + cut_position][col].set_wall()
                draw()
            grid[min_y + cut_position][min_x + gap_position].reset()
            draw()


        if cut_direction is VERTICAL:
            stack.append(((min_y, min_x), (max_y, min_x + cut_position - 1)))
            stack.append(((min_y, min_x + cut_position + 1), (max_y, max_x)))
        else:
            stack.append(((min_y, min_x), (min_y + cut_position - 1, max_x)))
            stack.append(((min_y + cut_position + 1, min_x), (max_y, max_x)))


### HELPER FUNCTIONS

def euclidean_dist(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x2 - x1) + abs(y2 - y1)

def make_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        if current.color != START_COLOR:
            current.set_path()
        draw()

def wall_edges(draw, grid):
    for i, row in enumerate(grid):
        for j, node in enumerate(row):
            if i == 0 or i == len(grid)-1:
                grid[i][j].set_wall()
                draw()
            elif j == 0 or j == len(row)-1:
                grid[i][j].set_wall()
                draw()
