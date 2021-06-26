#!/usr/bin/env python

"""
Gaming board
"""
import os

from daeqhipao.illegal_moves import *
import pygame
import images

IMAGE_DIR = os.path.dirname(images.__file__)
LOGO = os.path.join(IMAGE_DIR, 'logo.png')


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HIGHLIGHT = (170, 170, 170)

class Board:
    starting_squares = [(3, 9),
                        (4, 9),
                        (5, 9),
                        (6, 9),
                        (7, 9),
                        (1, 3),
                        (1, 4),
                        (1, 5),
                        (1, 6),
                        (1, 7),
                        (3, 1),
                        (4, 1),
                        (5, 1),
                        (6, 1),
                        (7, 1),
                        (9, 3),
                        (9, 4),
                        (9, 5),
                        (9, 6),
                        (9, 7)]

    temple_squares = [(0, 5), (0, 10), (5, 0), (5, 10)]

    temple_area_squares = [(3, 8),
                           (4, 8),
                           (5, 8),
                           (6, 8),
                           (7, 8),
                           (2, 3),
                           (2, 4),
                           (2, 5),
                           (2, 6),
                           (2, 7),
                           (3, 2),
                           (4, 2),
                           (5, 2),
                           (6, 2),
                           (7, 2),
                           (8, 3),
                           (8, 4),
                           (8, 5),
                           (8, 6),
                           (8, 7)]

    def __init__(self, screen, height):

        self.screen = screen
        self.square_width = int(height / 13)
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

        logo_position = (6 * self.square_width, 6 * self.square_width)
        logo = pygame.transform.smoothscale(self.logo, (self.square_width, self.square_width))
        self.screen.blit(logo, logo_position)

    def draw_board_line(self, start, end):
        start_x, start_y = start
        end_x, end_y = end

        start_x = self.square_width * (1 + start_x)
        start_y = self.square_width * (1 + start_y)

        end_x = self.square_width * (1 + end_x)
        end_y = self.square_width * (1 + end_y)

        pygame.draw.line(self.screen, BLACK, (start_x, start_y), (end_x, end_y))

    def check_field(self, mouse):
        x = int(mouse[0] / self.square_width) - 1
        y = int(mouse[1] / self.square_width) - 1

        field = self.get_field(x, y)

        if not field.type == 'no field':
            return field

        else:
            return None


    def highlight_field(self, mouse, highlight_colour=(170,170,170)):
        for i, row in enumerate(self.board):
            for j, column in enumerate(row):
                field = self.get_field(i, j)
                if not field.type == 'no field':
                    if field.rectangle.collidepoint(mouse):
                        hovered = True
                    else:
                        hovered = False
                    field.draw(self.screen, hovered)


    def calc_offset(self, field):
        x_offset = 100 + field.x * 100 + 3
        y_offset = 100 + field.y * 100 + 3

        return x_offset, y_offset

    def calc_symbol_offset(self, x_offset, y_offset):
        x_offset = x_offset + 25
        y_offset = y_offset + 25

        return x_offset, y_offset

    def draw_piece(self, piece):

        piece_type = piece.type.lower()

        if piece.gender == 'F':
            gender = 'female'
        else:
            gender = 'male'

        if not piece.active:
            piece_body_dir = f'pieces/{piece.player.colour}_passive.png'
        else:
            piece_body_dir = f'pieces/{piece.player.colour}_{gender}_{piece_type}.png'

        piece_image = Image.open(piece_body_dir)
        x_offset, y_offset = self.calc_offset(piece.location)
        self.image.paste(piece_image, box=(x_offset, y_offset))

        piece_symbol_dir = 'symbols/%s.png' % piece.name
        symbol_image = Image.open(piece_symbol_dir)
        x_offset, y_offset = self.calc_symbol_offset(x_offset, y_offset)
        self.image.paste(symbol_image, box=(x_offset, y_offset), mask=symbol_image)

    def draw_pieces(self, board):
        for row in board.board:
            for column in row:
                if column.piece:
                    self.draw_piece(column.piece)

    def draw_board(self, board):
        self.draw_frame()
        self.draw_pieces(board)

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


        for x, y in self.starting_squares:
            self.board[x][y].type = "starting square"

        for x, y in self.temple_area_squares:
            self.board[x][y].type = "temple area"

        for x, y in self.temple_squares:
            self.board[x][y].type = "temple square"

    def set_rectangles(self):
        for i, row in enumerate(self.board):
            for j, column in enumerate(row):
                self.board[i][j].set_rectangle(self.square_width)


    def print_board_type(self):
        string = ''
        for row in self.board:
            for column in row:
                string += "%s\t" % column.type
            string += '\n'
        print(string)

    def get_field(self, x, y):
        return self.board[x][y]


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
            pygame.draw.rect(screen, HIGHLIGHT, self.rectangle)
        else:
            pygame.draw.rect(screen, WHITE, self.rectangle)


    def set_owner(self, player):
        self.owner = player

    def in_temple_area(self):
        if self.type == 'temple area' or self.type == 'starting square':
            return True
        else:
            return False

    def activate_flame(self, piece):
        self.flame = True
        self.flame_casters.append(piece.player())

    def deactivate_flame(self):
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

    def get_adjacent_horizontal(self, board):

        adjacent = []

        coord_combinations = [(self.location.x - 1, self.location.y),
                              (self.location.x + 1, self.location.y),
                              (self.location.x, self.location.y - 1),
                              (self.location.x, self.location.y + 1)]


        for coord_combination in coord_combinations:
            x = coord_combination[0]
            y = coord_combination[1]
            
            try:
                candidate = PhantomField(x, y)
                board.check_field(candidate)
                adjacent.append(board.get_field(candidate))

            except IllegalField:
                pass

        return adjacent

    def get_adjacent_diagonal(self, board):

        adjacent = []

        coord_combinations = [(self.location.x - 1, self.location.y - 1),
                              (self.location.x + 1, self.location.y - 1),
                              (self.location.x - 1, self.location.y + 1),
                              (self.location.x + 1, self.location.y + 1)]


        for coord_combination in coord_combinations:
            x = coord_combination[0]
            y = coord_combination[1]
            
            try:
                candidate = PhantomField(x, y)
                board.check_field(candidate)
                adjacent.append(board.get_field(candidate))

            except IllegalField:
                pass

        return adjacent

    def get_adjacent(self, board):

        adjacent = []

        x_coords = [self.x - 1, self.x, self.x + 1]
        y_coords = [self.y - 1, self.y, self.y + 1]

        for x in x_coords:
            for y in y_coords:
                if not (x == self.x) and not (y == self.y):
                    try:
                        candidate = PhantomField(x, y)
                        check_field(candidate)
                        adjacent.append(board.get_field(candidate))

                    except IllegalField:
                        pass

        return adjacent

class PhantomField(Field):
    def __init__(self, x, y):
        Field.__init__(self, x, y)

class TempleSquare(Field):
    def __init__(self, x, y, player):
        Field.__init__(self, x, y)
        self.type = 'Temple'
        self.player = player
        self.mind = 0

    def set_mind(self, user):
        if user.legacy_duration:
            self.mind = 2
        else:
            self.mind = 1

    def countdown_mind(self):
        self.mind -= 1
        assert mind >= 0

class TempleArea(Field):
    def __init__(self, x, y, player, starter):
        Field.__init__(self, x, y)
        self.player = player
        self.type = "Temple Area"
        self.starter = starter
        
        

class NoField(Field):
    def __init__(self, x, y):
        Field.__init__(self, x, y)
        self.type = "No field"



if __name__ == "__main__":
    board = Board()
    board.print_board()
