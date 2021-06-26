import pygame

from daeqhipao.style import *

class SidePanel:
    def __init__(self, screen):
        self.screen = screen

    def draw_panel(self):
        pygame.draw.rect(self.screen, BACKGROUND_PANEL, PANEL)

class Button:
    def __init__(self, text, position, dimensions):
        self.text = text
        self.rectangle = pygame.Rect(position, dimensions)

    def highlight(self):
        pass

