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
        make choice
        select power
        select power target
        confirm or reset
        place barrier
        remove barrier

    """

    def __init__(self, players, board, screen, pieces, barriers):
        self.turn = 0
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
        self.hover = False

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
        hide_piece_buttons(self.screen, self.active_buttons)
        show_reset_selection_button(self.screen, self.active_buttons)
        target_type = self.power.get_target_type()

        self.board.highlight_field_strong(self.current_piece.player, target)

        if target_type == 'field':
            if self.power.selected_field_1:
                self.power.select_field_2(target)
            else:
                self.power.select_field_1(target)

        elif target_type == 'piece':

            if self.power.selected_piece_1:
                self.power.select_piece_2(target.piece)
            else:
                self.power.select_piece_1(target.piece)

        elif target_type == 'barrier':
            if self.power.selected_barrier_1:
                self.power.select_barrier_2(target.barrier)
            else:
                self.power.select_barrier_1(target.barrier)

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

            self.current_piece = None
            self.new_state('zaopeng')

            return True

        else:
            return False

    def place_zaopeng_barrier(self, field):
        barrier_to_place = self.barriers.unused_barriers[0]
        barrier_to_place.place_on_board(field, self.board, self.barriers)
        PLACE_BARRIER_BUTTON.selected = False

    def remove_zaopeng_barrier(self, field):
        barrier_to_remove = field.barrier
        barrier_to_remove.remove_from_board(self.board, self.barriers)
        REMOVE_BARRIER_BUTTON.selected = False

    def next_turn(self):
        hide_piece_buttons(self.screen, self.active_buttons)

        self.turn += 1
        for field in self.board.fields:
            if field.flame:
                field.countdown_flame(self.current_player)

        self.current_player = self.players[self.turn % len(self.players)]
        self.current_piece = None
        self.has_moved = False
        self.has_used_power = False
        self.reset_states()

        if self.zaopeng():
            self.new_state('zaopeng start turn')

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
                if piece.idea or piece.illusion:
                    self.selectable_fields = [piece.location]
                    break
                else:
                    self.selectable_fields.append(piece.location)

    def select_piece(self, piece):
        self.current_piece = piece
        self.movement_options = self.current_piece.get_movement_options(self.board)
        if self.current_piece.illusion:
            show_move_button(self.screen, self.active_buttons)
        else:
            show_piece_buttons(self.screen, self.active_buttons)
        self.new_state('select move or use power')

    def show_movement_options(self):
        self.board.highlight_fields(self.current_player, self.movement_options)

    def display_choices(self):
        hide_piece_buttons(self.screen, self.active_buttons)

        x = int(0.7 * HEIGHT)
        relative_position = 0.85
        dimensions = (int(0.2 * HEIGHT), int(HEIGHT / 25))

        for choice in self.power.get_choices(self.barriers):
            if choice:
                y = int(relative_position * HEIGHT)
                position = (x, y)
                button = ChoiceButton(choice, position, dimensions)
                show_power_choice_button(self.screen, self.active_buttons, button)

                relative_position += 0.05

    def show_power_targets(self):
        print("showing targets..")

        if self.current_target_fields:
            for field in self.current_target_fields:
                self.board.redraw_field(field, BACKGROUND_BOARD)

        self.power.highlight_selected_fields(self.screen, self.board)

        self.current_target_fields = self.power.get_target_fields(self.pieces, self.barriers, self.board, self.players)
        self.power.highlight_all_targets(self)

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
        if not self.current_piece.idea:
            show_end_turn_button(self.screen, self.active_buttons)
        if self.current_piece.illusion:
            show_power_button(self.screen, self.active_buttons)
        self.has_moved = True
        self.current_piece.deactivate_illusion()
        self.new_state('select use power or end turn')
        self.board.redraw_field(target_square, colour=HIGHLIGHT_BOARD)


    def random_click(self):
        state = self.get_current_state()

        if state in {'zaopeng', 'place barrier', 'place barrier start turn', 'remove barrier', 'remove barrier start turn'}:
            pass
        else:
            self.hover = False
            hide_piece_buttons(self.screen, self.active_buttons)
            if self.current_piece and self.has_moved:
                if not self.current_piece.idea:
                    show_end_turn_button(self.screen, self.active_buttons)
                show_power_button(self.screen, self.active_buttons)

            if self.current_piece and self.power and state =='select power target':
                self.reset_power()
            elif self.current_piece and self.has_moved and state == 'select use power or end turn':
                pass

            else:
                self.reset_piece_selection()


    def detect_click_location(self, mouse):

        field = self.board.get_mouse_field(mouse)
        button = get_mouse_button(self.active_buttons, mouse)

        if button:
            return button
        elif field:
            return field
        else:
            return None

    def new_state(self, state_type):
        self.state_nr += 1
        self.states.append(state_type)

    def reset_power(self):
        self.hover = False

        fields_to_redraw = []

        for possible_target in [self.power.selected_piece_1,
                                self.power.selected_piece_2,
                                self.power.selected_barrier_1,
                                self.power.selected_barrier_2,
                                self.power.selected_field_1,
                                self.power.selected_field_2]:
            if possible_target:
                if type(possible_target) == Field:
                    fields_to_redraw.append(possible_target)

                else:
                    fields_to_redraw.append(possible_target.location)

        fields_to_redraw += self.current_target_fields

        hide_piece_buttons(self.screen, self.active_buttons)

        self.power.reset_targets()
        self.has_used_power = False

        for field in fields_to_redraw:
            self.board.redraw_field(field, BACKGROUND_BOARD)

        if self.has_moved:
            if not self.current_piece.idea:
                show_end_turn_button(self.screen, self.active_buttons)
            show_power_button(self.screen, self.active_buttons)
            self.new_state('select use power or end turn')
        else:

            if self.current_piece.illusion:
                show_move_button(self.screen, self.active_buttons)
            else:
                show_piece_buttons(self.screen, self.active_buttons)
            self.new_state('select move or use power')


    def do_click_action(self, mouse):
        print(self.pieces.active_pieces)
        print(self.pieces.passive_pieces)
        state = self.get_current_state()
        selected_entity = self.detect_click_location(mouse)
        if selected_entity:
            if type(selected_entity) == Field:
                self.do_field_action(selected_entity)
            elif type(selected_entity) == Button or issubclass(type(selected_entity), Button):
                self.do_button_action(selected_entity, mouse)
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
                self.random_click()

        elif state == 'select power target':
            if field in self.current_target_fields:
                print("make selection")
                self.select_target(field)
                if self.power.target_nr > 0:
                    self.show_power_targets()
                    self.new_state('select power target')
                else:

                    self.ask_confirmation()
                    self.hover = False
            else:
                self.reset_power()

        elif state == 'place barrier' or state == 'place barrier start turn':
            if not field.occupied and not field.type == 'temple square':
                self.place_zaopeng_barrier(field)
            if state == 'place barrier':
                self.next_turn()
            else:
                self.reset_piece_selection()
                hide_piece_buttons(self.screen, self.active_buttons)

        elif state == 'remove barrier' or state == 'remove barrier start turn':
            if field.barrier:
                self.remove_zaopeng_barrier(field)
            if state == 'remove barrier':
                self.next_turn()
            else:
                self.reset_piece_selection()
                hide_piece_buttons(self.screen, self.active_buttons)

        elif state == 'select use power or end turn':
            self.random_click()

        elif state in {'select power', 'confirm or reset', 'make choice'}:
            self.reset_power()

        else:
            self.random_click()

    def select_power(self, button, mouse):
        self.power = button.power
        hide_piece_buttons(self.screen, self.active_buttons)

        if not self.power.start_with_choice:
            self.show_power_targets()
            self.new_state('select power target')
        else:
            self.display_choices()
            self.new_state('make choice')

    def make_choice(self, button):
        self.power.choice = button.text
        if self.power.choice == "Place 1 barrier" or self.power.choice == "Remove 1 barrier":
            self.power.target_nr -= 1
        hide_piece_buttons(self.screen, self.active_buttons)
        self.new_state('select power target')

    def do_button_action(self, button, mouse):
        state = self.get_current_state()
        if button.text == "MOVE":
            self.show_movement_options()
            self.new_state('select move')
        elif button.text == "USE POWER":
            for field in self.movement_options:
                if field.piece != self.current_piece:
                    self.board.redraw_field(field, BACKGROUND_BOARD)

            if self.current_piece.type == 'God':
                self.new_state('select power')
                self.show_power_options()
            elif self.current_piece.type == 'Heir':
                self.power = self.current_piece.power
                hide_piece_buttons(self.screen, self.active_buttons)
                show_reset_selection_button(self.screen, self.active_buttons)

                if self.power.fixed_affected_area:
                    self.current_target_fields = self.power.get_target_fields_1(self.board)
                    self.board.highlight_fields_strong(self.current_player, self.current_target_fields)
                    self.ask_confirmation()

                elif not self.power.start_with_choice:
                    self.show_power_targets()
                    self.new_state('select power target')

                else:
                    self.display_choices()
                    self.new_state('make choice')

        elif type(button) == PowerButton:

            self.select_power(button, mouse)

        elif type(button) == ChoiceButton:

            self.make_choice(button)
            self.show_power_targets()

        elif button.text == "CONFIRM":
            self.power.activate_power(self.pieces, self.barriers, self.board)
            self.current_target_fields = []

            if not self.zaopeng():
                self.next_turn()
        elif button.text == "END TURN":
            self.next_turn()
        elif button.text == "RESET SELECTION":
            self.reset_power()
        elif button.text == "PLACE BARRIER":
            button.selected = True
            REMOVE_BARRIER_BUTTON.selected = False
            if state in {'zaopeng', 'remove barrier'}:
                self.new_state('place barrier')
            elif state in {'zaopeng start turn', 'remove barrier start turn'}:
                self.new_state('place barrier start turn')
        elif button.text == "REMOVE BARRIER":
            button.selected = True
            PLACE_BARRIER_BUTTON.selected = False
            if state in {'zaopeng', 'place barrier'}:
                self.new_state('remove barrier')
            elif state in {'zaopeng start turn', 'place barrier start turn'}:
                self.new_state('remove barrier start turn')


        else:
            if state in {'select power', 'confirm or reset'}:
                self.reset_power()

            else:
                self.random_click()




