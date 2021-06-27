import pygame
from daeqhipao.style import *


class Button:
    def __init__(self, text, position, dimensions, font_size=None):
        self.text = text

        self.x, self.y = position
        self.width, self.height = dimensions
        self.rectangle = pygame.Rect(position, dimensions)
        self.font_size = font_size
        if not self.font_size:
            self.set_font_size()

        self.set_text_position()
        self.set_font()
        self.rendered_text = self.font.render(text, True, BUTTON_TEXT_COLOUR)

    def __hash__(self):
        return self.text

    def __eq__(self, other):
        return self.text == other.text

    def __repr__(self):
        return self.text

    def highlight(self, screen):
        pygame.draw.rect(screen, BUTTON_HIGHLIGHT_COLOUR, self.rectangle)
        pygame.draw.rect(screen, BLACK, self.rectangle, 2)
        screen.blit(self.rendered_text, (self.text_x, self.text_y))

    def draw(self, screen):
        pygame.draw.rect(screen, BUTTON_COLOUR, self.rectangle)
        pygame.draw.rect(screen, BLACK, self.rectangle, 2)
        screen.blit(self.rendered_text, (self.text_x, self.text_y))

    def erase_button(self, screen):
        pygame.draw.rect(screen, BACKGROUND_BOARD, self.rectangle)
        pygame.draw.rect(screen, BACKGROUND_BOARD, self.rectangle, 2)

    def set_font_size(self):
        max_width = (self.width - 10) / len(self.text)
        self.font_size = min([int(max_width / FONT_RATIOS[FONT]), self.height - 10])

    def set_text_position(self):
        self.text_x = self.x + int((self.width - (self.font_size * FONT_RATIOS[FONT] * len(self.text))) / 2)
        self.text_y = self.y + int((self.height - self.font_size) / 2)

    def set_font(self):
        self.font = pygame.font.SysFont(FONT, self.font_size, bold=True)


class MoveButton(Button):
    def __init__(self):
        position = (int(0.7 * HEIGHT), int(0.85 * HEIGHT))
        dimensions = (int(0.2 * HEIGHT), int(HEIGHT / 25))

        super().__init__("MOVE", position, dimensions)


class UsePowerButton(Button):
    def __init__(self):
        position = (int(0.7 * HEIGHT), int(0.90 * HEIGHT))
        dimensions = (int(0.2 * HEIGHT), int(HEIGHT / 25))

        super().__init__("USE POWER", position, dimensions)


MOVE_BUTTON = MoveButton()
POWER_BUTTON = UsePowerButton()


def highlight_buttons(active_buttons, screen, mouse):
    for button in active_buttons:
        if button.rectangle.collidepoint(mouse):
            button.highlight(screen)
        else:
            button.draw(screen)


def get_mouse_button(active_buttons, mouse):
    for button in active_buttons:
        if button.rectangle.collidepoint(mouse):
            return button

    return None


def make_buttons():
    buttons = []
    new_game = Button("NEW GAME", (HEIGHT + int(PANEL_WIDTH * 0.05), int(9.5 * HEIGHT / 10)), (int(PANEL_WIDTH * 0.9), int(HEIGHT / 25)))
    buttons.append(new_game)

    return buttons


def show_piece_buttons(screen, active_buttons):
    MOVE_BUTTON.draw(screen)
    POWER_BUTTON.draw(screen)
    active_buttons.append(MOVE_BUTTON)
    active_buttons.append(POWER_BUTTON)


def hide_piece_buttons(screen, active_buttons):
    try:
        active_buttons.remove(MOVE_BUTTON)
    except ValueError:
        pass

    try:
        active_buttons.remove(POWER_BUTTON)
    except ValueError:
        pass

    MOVE_BUTTON.erase_button(screen)
    POWER_BUTTON.erase_button(screen)







