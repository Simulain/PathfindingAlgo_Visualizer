import pygame
from CONST import *

class DropDown():
    def __init__(self, x, y, h, w, main="Select Algorithm", options=OPTION_LIST, color_menu=DROP_DOWN_MENU_COLOR,
                 color_option=DROP_DOWN_OPTION_COLOR, font=("Arial", 18)):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.SysFont(font[0], font[1])
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, window):
        pygame.draw.rect(window, self.color_menu[self.menu_active], self.rect, 0)
        pygame.draw.rect(window, BLACK, self.rect, 2)
        msg = self.font.render(self.main, True, BLACK)
        window.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(window, self.color_option[1 if i == self.active_option else 0], rect, 0)
                pygame.draw.rect(window, BLACK, rect, 2)
                msg = self.font.render(text, True, BLACK)
                window.blit(msg, msg.get_rect(center=rect.center))

    def update(self, mouse_pos):
        self.menu_active = self.rect.collidepoint(mouse_pos)
        self.active_option = -1

        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mouse_pos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

