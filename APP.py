from ALGO import *
from BUTTON import Button
from CONST import *
from DROPDOWN import DropDown
from NODE import Node


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIN_X, WIN_Y))
        self.running = True
        self.mouse_pos = None
        self.grid = []
        self.start = None
        self.end = None
        self.buttons = []
        self.drop_downs = []
        self.selected_algorithm = None

        pygame.display.set_caption("Pathfinding visualizer")

    def run(self):
        self.init_grid()
        self.load_elements()

        while self.running:
            self.update()
            self.events()
            self.draw()
            time.sleep(1. / 144)

### Draw Functions ###
    def draw(self):
        self.window.fill(WHITE)

        self.draw_buttons(self.window)
        self.draw_drop_downs(self.window)

        self.draw_nodes(self.window)
        self.draw_lines(self.window)
        pygame.display.update()

    def draw_buttons(self, window):
        for button in self.buttons:
            button.draw(window)

    def draw_drop_downs(self, window):
        for dd in self.drop_downs:
            dd.draw(window)

    def draw_nodes(self, window):
        for row in self.grid:
            for node in row:
                node.draw(window)

    def draw_lines(self, window):

        # Horizontal lines
        for i in range(BOARD_SIZE_Y):
            pygame.draw.line(window, GREY, (GRID_POS[0], GRID_POS[1] + SQUARE_SIZE * i),
                             (GRID_POS[0] + LINE_LENGTH_X, GRID_POS[1] + SQUARE_SIZE * i), 2)

        # Vertical lines
        for j in range(BOARD_SIZE_X):
            pygame.draw.line(window, GREY, (GRID_POS[0] + SQUARE_SIZE * j, GRID_POS[1]),
                             (GRID_POS[0] + SQUARE_SIZE * j, GRID_POS[1] + LINE_LENGTH_Y), 2)

        # Black borders
        pygame.draw.lines(window, BLACK, True, [(GRID_POS[0], GRID_POS[1]), (GRID_POS[0], GRID_POS[1] + LINE_LENGTH_Y),
                                                (GRID_POS[0] + LINE_LENGTH_X, GRID_POS[1] + LINE_LENGTH_Y),
                                                (GRID_POS[0] + LINE_LENGTH_X, GRID_POS[1])], 3)

### Game state functions ###
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # LMB
            if pygame.mouse.get_pressed()[0]:
                con_pos = self.convert_position(self.mouse_pos)
                if con_pos:
                    node = self.grid[int(con_pos[1])][int(con_pos[0])]
                    if self.start is None and node != self.end:
                        self.start = node
                        node.set_start()
                    elif self.end is None and node != self.start:
                        self.end = node
                        node.set_end()
                    elif node != self.start and node != self.end:
                        node.set_wall()
                else:
                    for button in self.buttons:
                        if button.highlighted:
                            self.button_handler(button)

                    for dd in self.drop_downs:
                        self.drop_down_handler(dd)

            # RMB
            elif pygame.mouse.get_pressed()[2]:
                con_pos = self.convert_position(self.mouse_pos)
                if con_pos:
                    node = self.grid[int(con_pos[1])][int(con_pos[0])]
                    if node == self.start:
                        self.start = None
                    elif node == self.end:
                        self.end = None
                    node.reset()

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(self.mouse_pos)

        for dd in self.drop_downs:
            dd.update(self.mouse_pos)

### Helper Functions ###
    def clear_walls(self):
        self.clear_visualization()

        for row in self.grid:
            for node in row:
                if node.is_wall():
                    node.reset()

    def clear_visualization(self):
        for row in self.grid:
            for node in row:
                node.visited = False
                if node.is_visualization():
                    node.reset()

    def clear_grid(self):
        self.start = None
        self.end = None
        self.init_grid()

    def init_grid(self):
        self.grid = []
        for i in range(BOARD_SIZE_Y):
            self.grid.append([])
            for j in range(BOARD_SIZE_X):
                node = Node(i, j)
                self.grid[i].append(node)

    def convert_position(self, pos):
        x = pos[0]
        y = pos[1]

        if x <= GRID_POS[0] or y <= GRID_POS[1]:
            return False
        elif x >= (GAME_X + GRID_POS[0]) or y >= (GAME_Y + GRID_POS[1]):
            return False
        return (x - GRID_POS[0])//SQUARE_SIZE, (y - GRID_POS[1])//SQUARE_SIZE

    def load_buttons(self):
        self.buttons.append(Button(2*EDGE_X, 2*EDGE_Y + LINE_LENGTH_Y, 40, 80, "Visualize", "Algorithm"))
        self.buttons.append(Button(4*EDGE_X, 2*EDGE_Y + LINE_LENGTH_Y, 40, 80, "Clear All", function=self.clear_grid))
        self.buttons.append(Button(6*EDGE_X, 2*EDGE_Y + LINE_LENGTH_Y, 40, 80, "Clear Walls", function=self.clear_walls))
        self.buttons.append(Button(8*EDGE_X, 2*EDGE_Y + LINE_LENGTH_Y, 40, 120, "Generate Maze", "Maze", function=make_maze))

    def load_drop_downs(self):
        self.drop_downs.append(DropDown(3/2*EDGE_X+LINE_LENGTH_X, 2*EDGE_Y, 40, 120))

    def load_elements(self):
        self.load_buttons()
        self.load_drop_downs()

    def button_handler(self, button):
        button.highlighted = False
        if button.type == "Algorithm" and self.prepare_algorithm() and self.selected_algorithm is not None:
            button.update_params((lambda: self.draw(), self.grid, self.start, self.end))
            button.function = self.selected_algorithm
            button.click()
        elif button.type == "Maze":
            button.update_params((lambda: self.draw(), self.grid))
            button.click()
        elif button.type == None:
            button.click()

    def drop_down_handler(self, drop_menu):
        if drop_menu.menu_active:
            drop_menu.draw_menu = not drop_menu.draw_menu
        elif drop_menu.draw_menu and drop_menu.active_option >= 0:
            drop_menu.draw_menu = False
            drop_menu.main = drop_menu.options[drop_menu.active_option]
            self.selected_algorithm = self.determine_algorithm(drop_menu.main)

    def prepare_algorithm(self):
        self.clear_visualization()

        if self.start != None and self.end != None:
            for row in self.grid:
                for node in row:
                    node.determine_adjacent(self.grid)
            return True

        return False

    def determine_algorithm(self, dd_selected):
        if dd_selected == OPTION_LIST[0]:
            return dijkstra
        elif dd_selected == OPTION_LIST[1]:
            return a_star
        elif dd_selected == OPTION_LIST[2]:
            return greedy_best_first
        elif dd_selected == OPTION_LIST[3]:
            return depth_first
        elif dd_selected == OPTION_LIST[4]:
            return breadth_first
