import pygame
from daeqhipao.buttons import *
from daeqhipao.fields import Field

class TurnManager:

    """
    States
        select piece
        select move or use power
        select move
        select use power or end turn
        select power
        select power target
        confirm or reset
        place barrier
        remove barrier

    """

    def __init__(self, players, board, screen, pieces, barriers):
        self.turn = 0
        print(self.turn)
        self.players = players

        self.board = board
        self.screen = screen
        self.pieces = pieces
        self.barriers = barriers

        self.used_barriers = []
        self.unused_barriers = []

        self.current_player = players[0]
        self.current_piece = None

        self.has_moved = False
        self.has_used_power = False

        self.active_buttons = make_buttons()
        self.current_target_fields = []

        self.set_selectable_fields()
        self.movement_options = []

        self.power = None

        self.states = ['select piece']
        self.state_nr = 0

    def reset_states(self):
        self.states = ['select piece']
        self.state_nr = 0

    def get_current_state(self):
        state = self.states[-1]
        return state

    def get_state(self, state_nr):
        state = self.states[state_nr]
        return state

    def select_target(self, target):
        target_type = self.power.get_target_type()

        print(target_type)
        print(self.power.target_nr)

        self.board.highlight_field_strong(self.current_piece.player, target)

        if target_type == 'field':
            if self.current_piece.power.selected_field_1:
                self.power.select_field_2(target, self.board)
            else:
                self.power.select_field_1(target, self.board)

        elif target_type == 'piece':

            if self.power.selected_piece_1:
                self.power.select_piece_2(target.piece, self.board)
            else:
                print("Hey handsome")
                self.power.select_piece_1(target.piece, self.board)

        elif target_type == 'barrier':
            if self.power.selected_barrier_1:
                self.power.select_barrier_2(target.barrier, self.board)
            else:
                self.power.select_barrier_1(target.barrier, self.board)

    def zaopeng(self):
        if self.pieces.check_zaopeng(self.current_player):
            hide_piece_buttons(self.screen, self.active_buttons)
            self.pieces.zaopeng(self.current_player)
            for piece in self.pieces.pieces:
                if piece.player == self.current_player:
                    self.board.draw_piece(piece)
            if self.barriers.unused_barriers:
                show_place_barrier_button(self.screen, self.active_buttons)
            if self.barriers.used_barriers:
                show_remove_barrier_button(self.screen, self.active_buttons)

            return True

        else:
            return False

    def place_zaopeng_barrier(self, field):
        barrier_to_place = self.barriers.unused_barriers[0]
        barrier_to_place.place_on_board(field, self.board, self.barriers)

    def remove_zaopeng_barrier(self, field):
        barrier_to_remove = field.barrier
        barrier_to_remove.remove_from_board(self.board, self.barriers)

    def next_turn(self):
        hide_piece_buttons(self.screen, self.active_buttons)

        self.turn += 1

        self.current_player = self.players[self.turn % len(self.players)]
        self.current_piece = None
        self.has_moved = False
        self.has_used_power = False
        self.reset_states()
        self.set_selectable_fields()

    def reset_piece_selection(self):
        if self.current_piece and self.power:
            self.power.reset_targets()
        self.current_piece = None
        self.has_moved = False
        self.has_used_power = False
        self.new_state('select piece')

    def set_selectable_fields(self):
        self.selectable_fields = []

        for piece in self.pieces.pieces:
            if piece.active and piece.player == self.current_player:
                self.selectable_fields.append(piece.location)

    def select_piece(self, piece):
        self.current_piece = piece
        self.movement_options = self.current_piece.get_movement_options(self.board)
        show_piece_buttons(self.screen, self.active_buttons)
        self.new_state('select move or use power')

    def show_movement_options(self):
        self.board.highlight_fields(self.current_player, self.movement_options)

    def show_power_targets(self):
        self.current_target_fields = self.power.get_target_fields(self.pieces, self.barriers, self.board)
        self.board.highlight_fields(self.current_player, self.current_target_fields)

    def show_power_options(self):
        hide_piece_buttons(self.screen, self.active_buttons)
        x = int(0.7 * HEIGHT)

        relative_position = 0.75

        dimensions = (int(0.2 * HEIGHT), int(HEIGHT / 25))

        for power in self.current_piece.powers:
            y = int(relative_position * HEIGHT)
            position = (x, y)
            button = PowerButton(position, dimensions, power)
            show_power_choice_button(self.screen, self.active_buttons, button)
            relative_position += 0.05

    def move_piece(self, target_square):

        for field in self.movement_options:
            self.board.redraw_field(field, BACKGROUND_BOARD)

        self.current_piece.move(target_square, self.board)
        hide_move_button(self.screen, self.active_buttons)
        show_end_turn_button(self.screen, self.active_buttons)
        self.has_moved = True
        self.new_state('select use power or end turn')
        self.board.redraw_field(target_square, colour=HIGHLIGHT_BOARD)


    def random_click(self):
        hide_piece_buttons(self.screen, self.active_buttons)
        if self.current_piece and self.has_moved:
            show_end_turn_button(self.screen, self.active_buttons)
            show_power_button(self.screen, self.active_buttons)

        else:
            self.reset_piece_selection()

    def detect_click_location(self, mouse):

        field = self.board.get_mouse_field(mouse)
        button = get_mouse_button(self.active_buttons, mouse)

        if field:
            return field
        elif button:
            return button
        else:
            return None

    def new_state(self, state_type):
        self.state_nr += 1
        self.states.append(state_type)

    def reset_power(self):

        for possible_target in [self.power.selected_piece_1,
                                self.power.selected_piece_2,
                                self.power.selected_barrier_1,
                                self.power.selected_barrier_2,
                                self.power.selected_field_1,
                                self.power.selected_field_2]:
            if possible_target:
                if type(possible_target) == Field:

                    self.board.redraw_field(possible_target, self.current_player.colour_rgb)
                else:
                    self.board.redraw_field(possible_target.location, self.current_player.colour_rgb)

        hide_piece_buttons(self.screen, self.active_buttons)

        self.power.reset_targets()
        self.has_used_power = False

        if self.has_moved:
            show_end_turn_button(self.screen, self.active_buttons)
            show_power_button(self.screen, self.active_buttons)
            self.new_state('select use power or end turn')
        else:
            show_piece_buttons(self.screen, self.active_buttons)
            self.new_state('select move or use power')


    def do_click_action(self, mouse):
        state = self.get_current_state()
        selected_entity = self.detect_click_location(mouse)
        print(selected_entity)
        if selected_entity:
            if type(selected_entity) == Field:
                self.do_field_action(selected_entity)
            elif type(selected_entity) == Button or issubclass(type(selected_entity), Button):
                self.do_button_action(selected_entity)
        else:
            if state in {'select power', 'confirm or reset'}:
                self.reset_power()

            elif state == 'select use power or end turn':
                self.random_click()
            else:
                self.random_click()

    def ask_confirmation(self):
        hide_piece_buttons(self.screen, self.active_buttons)
        show_confirm_button(self.screen, self.active_buttons)
        show_reset_selection_button(self.screen, self.active_buttons)
        self.new_state('confirm or reset')

    def do_field_action(self, field):
        state = self.get_current_state()
        if state == 'select piece':
            if field in self.selectable_fields:
                self.select_piece(field.piece)
            else:
                self.random_click()

        elif state == 'select move':
            if field in self.movement_options:
                self.move_piece(field)
            else:
                self.reset_piece_selection()

        elif state == 'select power target':
            if field in self.current_target_fields:
                self.select_target(field)
                if self.power.target_nr > 0:
                    self.new_state('select power target')
                else:
                    self.ask_confirmation()
            else:
                self.reset_power()

        elif state == 'place barrier':
            if not field.occupied and not field.type == 'temple square':
                self.place_zaopeng_barrier(field)
                self.next_turn()

        elif state == 'remove barrier':
            if field.barrier:
                self.remove_zaopeng_barrier(field)
                self.next_turn()


        elif state == 'select use power or end turn':
            self.random_click()

        elif state in {'select power', 'confirm or reset'}:
            self.reset_power()

        else:
            self.reset_piece_selection()

    def select_power(self, button):
        self.power = button.power
        self.new_state('select power target')

        hide_piece_buttons(self.screen, self.active_buttons)
        self.show_power_targets()

    def do_button_action(self, button):
        print(self.active_buttons)
        state = self.get_current_state()
        if button.text == "MOVE":
            self.show_movement_options()
            self.new_state('select move')
        elif button.text == "USE POWER":
            if self.current_piece.type == 'God':
                self.new_state('select power')
                self.show_power_options()
            elif self.current_piece.type == 'Heir':
                self.power = self.current_piece.power
                self.show_power_targets()
                self.new_state('select power target')
        elif type(button) == PowerButton:
            print("Entering..")

            self.select_power(button)

        elif button.text == "CONFIRM":
            self.power.activate_power(self.pieces, self.barriers, self.board)
            if not self.zaopeng():
                self.next_turn()
        elif button.text == "END TURN":
            self.next_turn()
        elif button.text == "RESET SELECTION":
            self.reset_power()
        elif button.text == "PLACE BARRIER":
            self.new_state('place barrier')
        elif button.text == "REMOVE BARRIER":
            self.new_state('remove barrier')
        else:
            if state in {'select power', 'confirm or reset'}:
                self.reset_power()

            else:
                self.reset_piece_selection()




