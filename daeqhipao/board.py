#!/usr/bin/env python

"""
Gaming board
"""
import os

from daeqhipao.illegal_moves import *
from daeqhipao.board_properties import BOARD_PROPERTIES
from daeqhipao.style import *
import pygame
import images.pieces

PIECE_IMAGE_DIR = os.path.dirname(images.pieces.__file__)
IMAGE_DIR = os.path.dirname(images.__file__)
LOGO = os.path.join(IMAGE_DIR, 'logo.png')


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

    def highlight_move_options(self, piece):
        legal_fields = piece.get_movement_options(self)
        for legal_field in legal_fields:
            legal_field.highlight(self.screen, piece.player, self)

        self.draw_frame()

    def highlight_fields(self, player, fields):

        for field in fields:
            field.highlight(self.screen, player, self)

        self.draw_frame()

    def highlight_field_strong(self, player, field):
        field.highlight_strong(self.screen, player, self)
        self.draw_frame()

    def highlight_field(self, mouse):
        for i, row in enumerate(self.board):
            for j, column in enumerate(row):
                field = self.get_field(i, j)
                if not field.type == 'no field':
                    if field.rectangle.collidepoint(mouse):
                        hovered = True
                    else:
                        hovered = False
                    field.draw(self.screen, hovered)
                    self.draw_frame()
                    if field.piece:
                        self.draw_piece(field.piece)

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

        if piece.gender == 'F':
            gender = 'female'
        else:
            gender = 'male'

        if not piece.active:
            piece_body_dir = os.path.join(PIECE_IMAGE_DIR, f'{piece.player.colour}_passive.png')
        else:
            piece_body_dir = os.path.join(PIECE_IMAGE_DIR, f'{piece.player.colour}_{gender}_{piece_type}.png')

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
        for i, row in enumerate(self.board):
            for j, column in enumerate(row):
                self.board[i][j].set_rectangle(SQUARE_WIDTH)


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


class Barriers:
    def __init__(self):
        self.count = 0
        
    def place_barrier(self, field, board):
        board.check_field(field)
        if self.count == 3:
            raise IllegalBarrier('count')
        if board.get_field(field).occupied:
            raise IllegalBarrier('occupied')
        if board.get_field(field).type == "Temple":
            raise IllegalBarrier('temple')

        board.get_field(field).barrier = True
        board.get_field(field).check_occupied()
        
        self.count += 1

    def move_barrier(self, old_field, new_field, board):
        board.check_field(new_field)
        board.check_field(old_field)
        
        if board.get_field(new_field).occupied:
            raise IllegalBarrier('occupied')
        if not board.get_field(old_field).barrier:
            raise IllegalBarrier('no barrier')
        if board.get_field(new_field).type == "Temple":
            raise IllegalBarrier('temple')

        board.get_field(old_field).barrier = False
        board.get_field(old_field).check_occupied()

        board.get_field(new_field).barrier = True
        board.get_field(new_field).check_occupied()

    def remove_barrier(self, field, board):
        board.check_field(field)
        if self.count == 0:
            raise IllegalBarrier('none')
        if not board.get_field(field).barrier:
            raise IllegalBarrier('no barrier')

        board.get_field(field).barrier = False
        board.get_field(field).check_occupied()

        self.count -= 1
        

class Field:
    """
    Field types:
        field
        no field
        temple square
        temple area
        starting square
        barrier square

    Owners:
        Player (1, 2, 3, 4)
        None

    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.owner = None
        self.type = 'field'

        self.piece = None
        self.barrier = False
        self.occupied = False
        
        self.ocean = False
        self.drought = False
        self.flame = False
        self.flame_casters = set([])
        
        self.type = 'Regular'
        self.rectangle = None

    def __repr__(self):
        return "%d-%d" % (self.x, self.y)

    def __eq__(self, field):
        return self.x == field.x and self.y == field.y

    def __hash__(self):
        return hash((self.x, self.y))

    def set_rectangle(self, square_width):
        x = (self.x + 1) * square_width
        y = (self.y + 1) * square_width
        self.rectangle = pygame.Rect(x, y, square_width, square_width)

    def draw(self, screen, hovered):
        if hovered:
            pygame.draw.rect(screen, HIGHLIGHT_BOARD, self.rectangle)
        else:
            pygame.draw.rect(screen, BACKGROUND_BOARD, self.rectangle)

    def highlight(self, screen, player, board):
        pygame.draw.rect(screen, player.colour_rgb, self.rectangle)
        if self.piece:
            board.draw_piece(self.piece)

    def highlight_strong(self, screen, player, board):
        pygame.draw.rect(screen, player.colour_rgb_strong, self.rectangle)
        if self.piece:
            board.draw_piece(self.piece)

    def set_ownership(self, player):
        self.owner = player

    def in_temple_area(self):
        if self.type == 'temple area' or self.type == 'starting square':
            return True
        else:
            return False

    def activate_flame(self, piece):
        self.flame = True
        self.flame_casters.add(piece.player())

    def deactivate_flame(self, piece):
        self.flame = False
        self.flame_casters.remove(piece.player())

    def check_occupied(self):
        if self.piece or self.barrier:
            self.occupied = True
        else:
            self.occupied = False

    def check_adjacent(self, field, board):
        diff_x = abs(self.x - field.x)
        diff_y = abs(self.y - field.y)

        if diff_x > 1:
            return False
        elif diff_y > 1:
            return False
        elif diff_x == 0 and diff_y == 0:
            return False
        else:
            return True

    def get_adjacent(self, board, type='all'):

        adjacent = []
        if type == 'horizontal':

            coord_combinations = [(self.x - 1, self.y),
                                  (self.x + 1, self.y),
                                  (self.x, self.y - 1),
                                  (self.x, self.y + 1)]

        elif type == 'diagonal':
            coord_combinations = [(self.x - 1, self.y - 1),
                                  (self.x + 1, self.y - 1),
                                  (self.x - 1, self.y + 1),
                                  (self.x + 1, self.y + 1)]

        elif type == 'all':
            coord_combinations = [(self.x - 1, self.y),
                                  (self.x + 1, self.y),
                                  (self.x, self.y - 1),
                                  (self.x, self.y + 1),
                                  (self.x - 1, self.y - 1),
                                  (self.x + 1, self.y - 1),
                                  (self.x - 1, self.y + 1),
                                  (self.x + 1, self.y + 1)]

        for coord_combination in coord_combinations:
            x = coord_combination[0]
            y = coord_combination[1]

            try:

                field = board.board[x][y]

                if field.type != 'no field':
                    adjacent.append(field)
            except IndexError:
                pass

        return adjacent

    def get_legal_adjacent(self, board, player, type='all'):

        adjacent = []

        fields = self.get_adjacent(board, type=type)

        for field in fields:

            if field.type != 'no field' and not field.piece and not field.barrier and not \
                    (field.type == 'temple square' and field.owner == player):
                adjacent.append(field)

        return adjacent


