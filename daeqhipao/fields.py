import pygame
from daeqhipao.style import *

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
        self.barrier = None
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

    def redraw(self, screen, colour):
        pygame.draw.rect(screen, colour, self.rectangle)

    def place_barrier(self, barrier):
        self.occupied = True
        self.barrier = barrier

    def remove_barrier(self, barrier):
        self.occupied = False
        self.barrier = None

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
        elif self.barrier:
            board.draw_barrier(self.barrier)

    def highlight_strong(self, screen, player, board):
        pygame.draw.rect(screen, player.colour_rgb_strong, self.rectangle)
        if self.piece:
            board.draw_piece(self.piece)
        elif self.barrier:
            board.draw_barrier(self.barrier)

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

    def check_legal_movement(self, piece):
        if self.type == 'no field':
            return False
        elif self.occupied:
            return False
        elif self.type == 'temple square' and self.owner == piece.player:
            return False
        elif self.ocean and piece.gender == 'female' and not piece.immune('Ocean'):
            return False
        elif self.drought and piece.gender == 'male' and not piece.immune('Drought'):
            return False
        elif self.flame and piece.player not in self.flame_casters and not piece.immune("Flame"):
            return False

        return True


    def get_legal_adjacent(self, board, piece):

        adjacent = []

        fields = self.get_adjacent(board, type=piece.movement_type)

        for field in fields:
            if field.check_legal_movement(piece):
                adjacent.append(field)

        return adjacent
