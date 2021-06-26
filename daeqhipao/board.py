#!/usr/bin/env python

"""
Gaming board
"""

from PIL import ImageDraw, ImageFont, Image
from illegal_moves import *

class Barriers():
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
        
        

        
class Field():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.piece = None
        self.barrier = False
        self.occupied = False
        
        self.ocean = False
        self.drought = False
        self.flame = False
        self.flame_casters = set([])
        
        self.type = 'Regular'

    def __repr__(self):
        return "%d-%d" % (self.x, self.y)

    def __eq__(self, field):
        return self.x == field.x and self.y == field.y

    def __hash__(self):
        return hash((self.x, self.y))

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
    

class Board():

    def __init__(self):
        self.board = []
        for i in range(11):
            row = []
            for j in range(11):
                row.append(Field(i, j))
            self.board.append(row)

        self.filter_board()
        self.define_squares()
        self.make_starter_dict()

    def make_starter_dict(self):
        self.starter_dict = {1: {1: self.get_field(PhantomField(3, 9)),
                                 2: self.get_field(PhantomField(4, 9)),
                                 3: self.get_field(PhantomField(5, 9)),
                                 4: self.get_field(PhantomField(6, 9)),
                                 5: self.get_field(PhantomField(7, 9))},
                             2: {1: self.get_field(PhantomField(1, 3)),
                                 2: self.get_field(PhantomField(1, 4)),
                                 3: self.get_field(PhantomField(1, 5)),
                                 4: self.get_field(PhantomField(1, 6)),
                                 5: self.get_field(PhantomField(1, 7))},
                             3: {1: self.get_field(PhantomField(3, 1)),
                                 2: self.get_field(PhantomField(4, 1)),
                                 3: self.get_field(PhantomField(5, 1)),
                                 4: self.get_field(PhantomField(6, 1)),
                                 5: self.get_field(PhantomField(7, 1))},
                             4: {1: self.get_field(PhantomField(9, 3)),
                                 2: self.get_field(PhantomField(9, 4)),
                                 3: self.get_field(PhantomField(9, 5)),
                                 4: self.get_field(PhantomField(9, 6)),
                                 5: self.get_field(PhantomField(9, 7))}}

    def get_starting_positions(self, player):
        return self.starter_dict[player.id]

    def filter_board(self):
        for i, row in enumerate(self.board):
            for j, column in enumerate(row):
                if i == 0 or i == 10:
                    if j != 5:
                        self.board[i][j] = NoField(i, j)

                elif j == 0 or j == 10:
                    if i != 5:
                        self.board[i][j] = NoField(i, j)
                        

                elif i == 1 or i == 2 or i == 8 or i == 9:
                    if j == 1 or j == 2 or j == 8 or j == 9:
                        self.board[i][j] = NoField(i, j)
                elif i == 5 and j == 5:
                    self.board[i][j] = NoField(i, j)

    def print_board_type(self):
        string = ''
        for row in self.board:
            for column in row:
                string += "%s\t" % column.type
            string += '\n'
        print(string)
        
    def get_field(self, field):
        return self.board[field.x][field.y]

    def check_field(self, field):

        if field.x < 0 or field.y < 0 or field.x > 10 or field.y > 10:
            raise IllegalField('no field')

        if self.get_field(field).type == "No field":
            raise IllegalField('no field')

    def get_temple_square(self, player):
        for row in self.board:
            for field in row:
                if field.type == "Temple":
                    if field.player == player.id:
                        return field

    def define_squares(self):
        for i, row in enumerate(self.board):
            for j, column in enumerate(row):
                if column.type != "No field":
                    if column.x == 0:
                        self.board[i][j] = TempleSquare(column.x, column.y, 2)
                    if column.y == 0:
                        self.board[i][j] = TempleSquare(column.x, column.y, 3)
                    if column.x == 10:
                        self.board[i][j] = TempleSquare(column.x, column.y, 4)
                    if column.y == 10:
                        self.board[i][j] = TempleSquare(column.x, column.y, 1)

                    if column.x == 1:
                        self.board[i][j] = TempleArea(column.x, column.y, 2,
                                                      True)
                    if column.x == 2:
                        self.board[i][j] = TempleArea(column.x, column.y, 2,
                                                      False)
                    if column.y == 1:
                        self.board[i][j] = TempleArea(column.x, column.y, 3,
                                                      True)
                    if column.y == 2:
                        self.board[i][j] = TempleArea(column.x, column.y, 3,
                                                      False)
                    if column.x == 8:
                        self.board[i][j] = TempleArea(column.x, column.y, 4,
                                                      False)
                    if column.x == 9:
                        self.board[i][j] = TempleArea(column.x, column.y, 4,
                                                      True)
                    if column.y == 8:
                        self.board[i][j] = TempleArea(column.x, column.y, 1,
                                                      False)
                    if column.y == 9:
                        self.board[i][j] = TempleArea(column.x, column.y, 1,
                                                      True)



if __name__ == "__main__":
    board = Board()
    board.print_board()
