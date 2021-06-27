import pygame
from daeqhipao.style import *

class Barrier:
    def __init__(self, barrier_id):
        self.id = barrier_id
        self.on_board = False
        self.location = None
        self.rectangle = None

    def __repr__(self):
        return f'Barrier {self.id}'

    def __eq__(self, barrier):
        return self.id == barrier.id

    def __hash__(self):
        return self.id

    def set_rectangle(self):
        x = (1 + self.location.x) * SQUARE_WIDTH + BARRIER_PADDING
        y = (1 + self.location.y) * SQUARE_WIDTH + BARRIER_PADDING
        self.rectangle = pygame.Rect(x, y, BARRIER_SIZE, BARRIER_SIZE)

    def place_on_board(self, field, board, barriers):
        if not field.occupied and field.type != 'temple square':
            self.on_board = True
            self.location = field
            field.place_barrier(self)
            barriers.set_used_and_unused_barriers()
            self.set_rectangle()
            board.draw_barrier(self)

    def remove_from_board(self, board, barriers):
        original_x = self.location.x
        original_y = self.location.y

        original_field = board.get_field(original_x, original_y)

        self.on_board = False
        self.location.remove_barrier(self)
        self.location = None
        barriers.set_used_and_unused_barriers()
        self.rectangle = None

        board.redraw_field(original_field, BACKGROUND_BOARD)


    def move(self, field, board):
        if not field.occupied and field.type != 'temple square' and field.type != 'no field':
            original_x = self.location.x
            original_y = self.location.y

            original_field = board.get_field(original_x, original_y)

            x_diff = field.x - self.location.x
            y_diff = field.y - self.location.y
            self.location.remove_barrier(self)
            self.location = field
            field.place_barrier(self)

            self.rectangle = self.rectangle.move(x_diff * SQUARE_WIDTH, y_diff * SQUARE_WIDTH)
            board.redraw_field(original_field, BACKGROUND_BOARD)
            board.draw_barrier(self)


class Barriers:
    def __init__(self, barriers):
        self.barriers = barriers
        self.used_barriers = []
        self.unused_barriers = []
        self.set_used_and_unused_barriers()

    def set_used_and_unused_barriers(self):

        self.used_barriers = []
        self.unused_barriers = []

        for barrier in self.barriers:
            if barrier.on_board:
                self.used_barriers.append(barrier)
            else:
                self.unused_barriers.append(barrier)

BARRIERS = Barriers([Barrier(1), Barrier(2), Barrier(3)])