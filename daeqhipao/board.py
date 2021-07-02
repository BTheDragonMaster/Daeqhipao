#!/usr/bin/env python

"""
Gaming board
"""
import os

import pygame
import images.pieces

from daeqhipao.illegal_moves import *
from daeqhipao.board_properties import BOARD_PROPERTIES
from daeqhipao.style import *
from daeqhipao.fields import Field
from daeqhipao.barriers import Barrier
from daeqhipao.pieces import Piece


PIECE_IMAGE_DIR = os.path.dirname(images.pieces.__file__)
IMAGE_DIR = os.path.dirname(images.__file__)
LOGO = os.path.join(IMAGE_DIR, 'logo.png')
BARRIER_LOGO = os.path.join(IMAGE_DIR, 'barrier.png')


class Board:

    def __init__(self, screen):

        self.screen = screen
        self.logo = pygame.image.load(LOGO)

        self.board = []
        for i in range(11):
            row = []
            for j in range(11):
                row.append(Field(i, j))
            self.board.append(row)

        self.assign_field_types()
        self.set_all_fields()
        self.set_rectangles()


    def draw_frame(self):
        self.draw_board_line((5, 0), (6, 0))
        self.draw_board_line((3, 1), (8, 1))
        self.draw_board_line((3, 2), (8, 2))
        self.draw_board_line((1, 3), (10, 3))
        self.draw_board_line((3, 1), (8, 1))
        self.draw_board_line((1, 4), (10, 4))
        self.draw_board_line((0, 5), (11, 5))
        self.draw_board_line((0, 6), (11, 6))
        self.draw_board_line((1, 7), (10, 7))
        self.draw_board_line((1, 8), (10, 8))
        self.draw_board_line((3, 9), (8, 9))
        self.draw_board_line((3, 10), (8, 10))
        self.draw_board_line((5, 11), (6, 11))

        self.draw_board_line((0, 5), (0, 6))
        self.draw_board_line((1, 3), (1, 8))
        self.draw_board_line((2, 3), (2, 8))
        self.draw_board_line((3, 1), (3, 10))
        self.draw_board_line((4, 1), (4, 10))
        self.draw_board_line((5, 0), (5, 11))
        self.draw_board_line((6, 0), (6, 11))
        self.draw_board_line((7, 1), (7, 10))
        self.draw_board_line((8, 1), (8, 10))
        self.draw_board_line((9, 3), (9, 8))
        self.draw_board_line((10, 3), (10, 8))
        self.draw_board_line((11, 5), (11, 6))

        logo_position = (6 * SQUARE_WIDTH, 6 * SQUARE_WIDTH)
        logo = pygame.transform.smoothscale(self.logo, (SQUARE_WIDTH, SQUARE_WIDTH))
        self.screen.blit(logo, logo_position)

    def draw_board_line(self, start, end):
        start_x, start_y = start
        end_x, end_y = end

        start_x = SQUARE_WIDTH * (1 + start_x)
        start_y = SQUARE_WIDTH * (1 + start_y)

        end_x = SQUARE_WIDTH * (1 + end_x)
        end_y = SQUARE_WIDTH * (1 + end_y)

        pygame.draw.line(self.screen, BLACK, (start_x, start_y), (end_x, end_y))

    def get_mouse_field(self, mouse):
        x = int(mouse[0] / SQUARE_WIDTH) - 1
        y = int(mouse[1] / SQUARE_WIDTH) - 1

        field = self.get_field(x, y)

        if field and not field.type == 'no field':
            return field

        else:
            return None

    def draw_barrier(self, barrier):
        barrier_image = pygame.image.load(BARRIER_LOGO)
        barrier_image_scaled = pygame.transform.smoothscale(barrier_image, (BARRIER_SIZE, BARRIER_SIZE))

        self.screen.blit(barrier_image_scaled, barrier.rectangle)

        self.draw_frame()

    def highlight_move_options(self, piece):
        legal_fields = piece.get_movement_options(self)
        for legal_field in legal_fields:
            legal_field.highlight(self.screen, piece.player, self)

        self.draw_frame()

    def redraw_field(self, field, colour):
        field.redraw(self.screen, colour)
        field.draw_conditions(self.screen)
        if field.piece:
            self.draw_piece(field.piece)

        elif field.barrier:
            self.draw_barrier(field.barrier)

        self.draw_frame()

    def highlight_fields(self, player, fields):

        for field in fields:
            field.highlight(self.screen, player, self)

        self.draw_frame()

    def highlight_fields_strong(self, player, fields):
        for field in fields:
            field.highlight_strong(self.screen, player, self)

        self.draw_frame()

    def highlight_field_strong(self, player, field):
        field.highlight_strong(self.screen, player, self)
        self.draw_frame()

    def set_all_fields(self):
        self.fields = []
        for i, row in enumerate(self.board):
            for j, column in enumerate(row):
                field = self.get_field(i, j)
                if not field.type == 'no field':
                    self.fields.append(field)

    def highlight_field(self, mouse):
        for field in self.fields:
            if field.rectangle.collidepoint(mouse):
                hovered = True
            else:
                hovered = False
            field.draw(self.screen, hovered)
            field.draw_conditions(self.screen)
            self.draw_frame()
            if field.piece:
                self.draw_piece(field.piece)
            elif field.barrier:
                self.draw_barrier(field.barrier)

    def calc_piece_offset(self, field):
        x_offset = (1 + field.x) * SQUARE_WIDTH + PIECE_PADDING
        y_offset = (1 + field.y) * SQUARE_WIDTH + PIECE_PADDING

        return x_offset, y_offset

    def calc_symbol_offset(self, field):
        x_offset = (1 + field.x) * SQUARE_WIDTH + SYMBOL_PADDING
        y_offset = (1 + field.y) * SQUARE_WIDTH + SYMBOL_PADDING

        return x_offset, y_offset

    def draw_piece(self, piece):

        piece_type = piece.type.lower()

        if not piece.active:
            piece_body_dir = os.path.join(PIECE_IMAGE_DIR, f'{piece.player.colour}_passive.png')
        else:
            piece_body_dir = os.path.join(PIECE_IMAGE_DIR, f'{piece.player.colour}_{piece.gender}_{piece_type}.png')

        piece_image = pygame.image.load(piece_body_dir)
        piece_image_scaled = pygame.transform.smoothscale(piece_image, (PIECE_SIZE, PIECE_SIZE))

        self.screen.blit(piece_image_scaled, piece.piece_rectangle)

        symbol_image = piece.symbol_image
        symbol_image_scaled = pygame.transform.smoothscale(symbol_image, (SYMBOL_SIZE, SYMBOL_SIZE))

        self.screen.blit(symbol_image_scaled, piece.symbol_rectangle)

    def draw_pieces(self):
        for row in self.board:
            for field in row:
                if field.piece:
                    self.draw_piece(field.piece)

    def draw_board(self):
        self.draw_frame()
        self.draw_pieces()

    def assign_field_types(self):
        for i, row in enumerate(self.board):
            for j, column in enumerate(row):
                if i == 0 or i == 10:
                    if j != 5:
                        self.board[i][j].type = "no field"

                elif j == 0 or j == 10:
                    if i != 5:
                        self.board[i][j].type = "no field"


                elif i == 1 or i == 2 or i == 8 or i == 9:
                    if j == 1 or j == 2 or j == 8 or j == 9:
                        self.board[i][j].type = "no field"
                elif i == 5 and j == 5:
                    self.board[i][j].type = "no field"


        for x, y in BOARD_PROPERTIES.starting_squares:
            self.board[x][y].type = "starting square"

        for x, y in BOARD_PROPERTIES.temple_area_squares:
            self.board[x][y].type = "temple area"

        for x, y in BOARD_PROPERTIES.temple_squares:
            self.board[x][y].type = "temple square"

    def set_rectangles(self):
        for field in self.fields:
            field.set_rectangle(SQUARE_WIDTH)

    def print_board_type(self):
        string = ''
        for row in self.board:
            for column in row:
                string += "%s\t" % column.type
            string += '\n'
        print(string)

    def get_field(self, x, y):
        try:
            return self.board[x][y]
        except IndexError:
            return None

    def swap_objects(self, object_1, object_2):
        source_x = object_1.location.x
        source_y = object_1.location.y

        target_x = object_2.location.x
        target_y = object_2.location.y

        source_location = self.get_field(source_x, source_y)
        target_location = self.get_field(target_x, target_y)

        x_diff_1 = target_location.x - object_1.location.x
        y_diff_1 = target_location.y - object_1.location.y

        x_diff_2 = -x_diff_1
        y_diff_2 = -y_diff_1

        if type(object_1) == Barrier:
            source_location.barrier = None

        elif issubclass(type(object_1), Piece):
            source_location.piece = None

        if type(object_2) == Barrier:
            target_location.barrier = None

        elif issubclass(type(object_2), Piece):
            target_location.piece = None

        if type(object_1) == Barrier:
            target_location.barrier = object_1

        elif issubclass(type(object_1), Piece):
            target_location.piece = object_1

        if type(object_2) == Barrier:
            source_location.barrier = object_2

        elif issubclass(type(object_2), Piece):
            source_location.piece = object_2

        if issubclass(type(object_1), Piece):
            object_1.piece_rectangle = object_1.piece_rectangle.move(x_diff_1 * SQUARE_WIDTH, y_diff_1 * SQUARE_WIDTH)
            object_1.symbol_rectangle = object_1.symbol_rectangle.move(x_diff_1 * SQUARE_WIDTH, y_diff_1 * SQUARE_WIDTH)
            self.draw_piece(object_1)
        elif type(object_1) == Barrier:
            object_1.rectangle = object_1.rectangle.move(x_diff_1 * SQUARE_WIDTH, y_diff_1 * SQUARE_WIDTH)
            self.draw_barrier(object_1)

        if issubclass(type(object_2), Piece):
            object_2.piece_rectangle = object_2.piece_rectangle.move(x_diff_2 * SQUARE_WIDTH, y_diff_2 * SQUARE_WIDTH)
            object_2.symbol_rectangle = object_2.symbol_rectangle.move(x_diff_2 * SQUARE_WIDTH, y_diff_2 * SQUARE_WIDTH)
            self.draw_piece(object_2)
        elif type(object_2) == Barrier:
            object_2.rectangle = object_2.rectangle.move(x_diff_2 * SQUARE_WIDTH, y_diff_2 * SQUARE_WIDTH)
            self.draw_barrier(object_2)

        object_1.location = target_location
        object_2.location = source_location

        print(source_location.piece)
        print(target_location.piece)




