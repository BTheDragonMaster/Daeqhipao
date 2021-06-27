import pygame

from daeqhipao.style import *


class SidePanel:
    def __init__(self, screen):
        self.screen = screen

    def draw_panel(self):
        pygame.draw.rect(self.screen, BACKGROUND_PANEL, PANEL)






