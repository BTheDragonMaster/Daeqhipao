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
        self.selected = False

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

class PowerButton(Button):
    def __init__(self, position, dimensions, power):
        self.power = power
        super().__init__(power.name, position, dimensions)

class ChoiceButton(Button):
    def __init__(self, text, position, dimensions):
        super().__init__(text, position, dimensions)


class UsePowerButton(Button):
    def __init__(self):
        position = (int(0.7 * HEIGHT), int(0.90 * HEIGHT))
        dimensions = (int(0.2 * HEIGHT), int(HEIGHT / 25))

        super().__init__("USE POWER", position, dimensions)

class EndTurnButton(Button):
    def __init__(self):
        position = (int(0.7 * HEIGHT), int(0.85 * HEIGHT))
        dimensions = (int(0.2 * HEIGHT), int(HEIGHT / 25))

        super().__init__("END TURN", position, dimensions)

class ResetSelectionButton(Button):
    def __init__(self):
        position = (int(0.7 * HEIGHT), int(0.85 * HEIGHT))
        dimensions = (int(0.2 * HEIGHT), int(HEIGHT / 25))

        super().__init__("RESET SELECTION", position, dimensions)


class ConfirmButton(Button):
    def __init__(self):
        position = (int(0.7 * HEIGHT), int(0.90 * HEIGHT))
        dimensions = (int(0.2 * HEIGHT), int(HEIGHT / 25))

        super().__init__("CONFIRM", position, dimensions)

class BackButton(Button):
    def __init__(self):
        position = (int(0.1 * HEIGHT), int(0.90 * HEIGHT))
        dimensions = (int(0.2 * HEIGHT), int(HEIGHT / 25))

        super().__init__("BACK", position, dimensions)

class PlaceBarrierButton(Button):
    def __init__(self):
        position = (int(0.7 * HEIGHT), int(0.85 * HEIGHT))
        dimensions = (int(0.2 * HEIGHT), int(HEIGHT / 25))

        super().__init__("PLACE BARRIER", position, dimensions)

class RemoveBarrierButton(Button):
    def __init__(self):
        position = (int(0.7 * HEIGHT), int(0.90 * HEIGHT))
        dimensions = (int(0.2 * HEIGHT), int(HEIGHT / 25))

        super().__init__("REMOVE BARRIER", position, dimensions)




MOVE_BUTTON = MoveButton()
POWER_BUTTON = UsePowerButton()
END_TURN_BUTTON = EndTurnButton()
CONFIRM_BUTTON = ConfirmButton()
RESET_SELECTION_BUTTON = ResetSelectionButton()
BACK_BUTTON = BackButton()
PLACE_BARRIER_BUTTON = PlaceBarrierButton()
REMOVE_BARRIER_BUTTON = RemoveBarrierButton()


def highlight_buttons(active_buttons, screen, mouse):
    for button in active_buttons:
        if button.rectangle.collidepoint(mouse) or button.selected:
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

def show_move_button(screen, active_buttons):
    MOVE_BUTTON.draw(screen)
    active_buttons.append(MOVE_BUTTON)

def show_end_turn_button(screen, active_buttons):
    END_TURN_BUTTON.draw(screen)
    active_buttons.append(END_TURN_BUTTON)

def show_power_button(screen, active_buttons):
    POWER_BUTTON.draw(screen)
    active_buttons.append(POWER_BUTTON)

def show_confirm_button(screen, active_buttons):
    CONFIRM_BUTTON.draw(screen)
    active_buttons.append(CONFIRM_BUTTON)

def show_reset_selection_button(screen, active_buttons):
    RESET_SELECTION_BUTTON.draw(screen)
    active_buttons.append(RESET_SELECTION_BUTTON)

def show_back_button(screen, active_buttons):
    BACK_BUTTON.draw(screen)
    active_buttons.append(BACK_BUTTON)

def hide_back_button(screen, active_buttons):
    hide_button(BACK_BUTTON, screen, active_buttons)


def hide_piece_buttons(screen, active_buttons):
    hide_button(MOVE_BUTTON, screen, active_buttons)
    hide_button(POWER_BUTTON, screen, active_buttons)
    hide_button(END_TURN_BUTTON, screen, active_buttons)
    hide_button(RESET_SELECTION_BUTTON, screen, active_buttons)
    hide_button(CONFIRM_BUTTON, screen, active_buttons)
    hide_button(PLACE_BARRIER_BUTTON, screen, active_buttons)
    hide_button(REMOVE_BARRIER_BUTTON, screen, active_buttons)
    hide_power_buttons(screen, active_buttons)
    hide_choice_buttons(screen, active_buttons)

def hide_power_buttons(screen, active_buttons):
    buttons_to_remove = []
    for i, button in enumerate(active_buttons[:]):
        if type(button) == PowerButton:
            buttons_to_remove.append(button)

    for button in buttons_to_remove:
        hide_button(button, screen, active_buttons)

def hide_choice_buttons(screen, active_buttons):
    buttons_to_remove = []
    for i, button in enumerate(active_buttons[:]):
        if type(button) == ChoiceButton:
            buttons_to_remove.append(button)

    for button in buttons_to_remove:
        hide_button(button, screen, active_buttons)

def hide_move_button(screen, active_buttons):
    hide_button(MOVE_BUTTON, screen, active_buttons)

def hide_power_button(screen, active_buttons):
    hide_button(POWER_BUTTON, screen, active_buttons)

def show_power_choice_button(screen, active_buttons, button):
    button.draw(screen)
    active_buttons.append(button)

def show_remove_barrier_button(screen, active_buttons):

    REMOVE_BARRIER_BUTTON.draw(screen)
    active_buttons.append(REMOVE_BARRIER_BUTTON)

def show_place_barrier_button(screen, active_buttons):

    PLACE_BARRIER_BUTTON.draw(screen)
    active_buttons.append(PLACE_BARRIER_BUTTON)

def hide_remove_barrier_button(screen, active_buttons):
    hide_button(REMOVE_BARRIER_BUTTON, screen, active_buttons)

def hide_place_barrier_button(screen, active_buttons):
    hide_button(PLACE_BARRIER_BUTTON, screen, active_buttons)

def hide_button(button, screen, active_buttons):
    try:
        active_buttons.remove(button)
    except ValueError:
        pass

    button.erase_button(screen)









