import pygame
from CONST import *


class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * SQUARE_SIZE + GRID_POS[0]
        self.y = row * SQUARE_SIZE + GRID_POS[1]
        self.color = WHITE
        self.adjacent = []
        self.visited = False

    def set_start(self):
        self.color = START_COLOR

    def set_end(self):
        self.color = END_COLOR

    def set_wall(self):
        self.color = WALL_COLOR

    def set_open(self):
        self.color = OPEN_COLOR

    def set_closed(self):
        self.color = CLOSED_COLOR

    def set_path(self):
        self.color = PATH_COLOR

    def set_visited(self):
        self.visited = True

    def is_wall(self):
        return self.color == WALL_COLOR

    def is_visualization(self):
        if self.color in VISUALIZATION_COLORS:
            return True

        return False

    def is_visited(self):
        return self.visited

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.color = WHITE

    def __lt__(self, other):
        return False

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE))

    def determine_adjacent(self, grid):
        self.adjacent = []
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.adjacent.append(grid[self.row - 1][self.col])

        if self.row < BOARD_SIZE_Y - 1 and not grid[self.row + 1][self.col].is_wall():
            self.adjacent.append(grid[self.row + 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.adjacent.append(grid[self.row][self.col - 1])

        if self.col < BOARD_SIZE_X - 1 and not grid[self.row][self.col + 1].is_wall():
            self.adjacent.append(grid[self.row][self.col + 1])
