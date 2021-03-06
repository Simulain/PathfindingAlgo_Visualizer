from CONST import *
import pygame

class Button:
    def __init__(self, x, y, height, width, text=None, type=None, font=("Arial", 18), color=BUTTON_COLOR,
                 highlighted_color=BUTTON_HIGHLIGHT, function=None, params=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.highlighted_color = highlighted_color
        self.text = text
        self.font = pygame.font.SysFont(font[0], font[1])
        self.function = function
        self.params = params
        self.highlighted = False
        self.type = type

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.highlighted = True
        else:
            self.highlighted = False

    def draw(self, window):
        color = self.color
        if self.highlighted:
            color = self.highlighted_color

        pygame.draw.rect(window, color, self.rect, 0)
        pygame.draw.rect(window, BLACK, self.rect, 2)
        msg = self.font.render(self.text, True, BLACK)
        window.blit(msg, msg.get_rect(center = self.rect.center))

    def click(self):
        if self.params:
            self.function(*self.params)
        else:
            self.function()

    def update_params(self, params):
        self.params = params
