import pygame
import os
from daeqhipao.style import *
import images.conditions

CONDITION_IMAGE_DIR = os.path.dirname(images.conditions.__file__)
print(CONDITION_IMAGE_DIR)
OCEAN_IMAGE = pygame.image.load(os.path.join(CONDITION_IMAGE_DIR, 'ocean.svg'))
DROUGHT_IMAGE = pygame.image.load(os.path.join(CONDITION_IMAGE_DIR, 'drought.svg'))
FLAME_IMAGE = pygame.image.load(os.path.join(CONDITION_IMAGE_DIR, 'flame.svg'))

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
        self.flame_casters = set()
        self.ocean_casters = set()
        self.drought_casters = set()

        self.type = 'Regular'
        self.rectangle = None
        self.ocean_rectangle = None
        self.drought_rectangle = None
        self.flame_rectangle = None

    def __repr__(self):
        return "%d-%d" % (self.x, self.y)

    def __eq__(self, field):
        if type(self) == type(field):
            if self.x == field.x and self.y == field.y:
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):
        return hash((self.x, self.y))

    def draw_conditions(self, screen):
        if self.ocean:
            ocean_image_scaled = pygame.transform.smoothscale(OCEAN_IMAGE, (CONDITION_SIZE, CONDITION_SIZE))
            screen.blit(ocean_image_scaled, self.ocean_rectangle)
        if self.drought:
            drought_image_scaled = pygame.transform.smoothscale(DROUGHT_IMAGE, (CONDITION_SIZE, CONDITION_SIZE))
            screen.blit(drought_image_scaled, self.drought_rectangle)
        if self.flame:
            flame_image_scaled = pygame.transform.smoothscale(FLAME_IMAGE, (CONDITION_SIZE, CONDITION_SIZE))
            screen.blit(flame_image_scaled, self.flame_rectangle)

    def activate_ocean(self, piece):
        self.ocean = True
        self.ocean_casters.add(piece)
        piece.ocean_fields.add(self)

    def deactivate_ocean(self, piece):
        self.ocean_casters.remove(piece)
        if not self.ocean_casters:
            self.ocean = False

    def activate_drought(self, piece):
        self.drought = True
        self.drought_casters.add(piece)
        piece.drought_fields.add(self)

    def deactivate_drought(self, piece):
        self.drought_casters.remove(piece)
        if not self.drought_casters:
            self.drought = False

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
        self.ocean_rectangle = pygame.Rect(x, y + 4 * CONDITION_SIZE, CONDITION_SIZE, CONDITION_SIZE)
        self.drought_rectangle = pygame.Rect(x + 4 * CONDITION_SIZE, y + 4 * CONDITION_SIZE, CONDITION_SIZE, CONDITION_SIZE)
        self.flame_rectangle = pygame.Rect(x, y, CONDITION_SIZE, CONDITION_SIZE)

    def draw(self, screen, hovered, highlight_colour=HIGHLIGHT_BOARD):
        if hovered:
            pygame.draw.rect(screen, highlight_colour, self.rectangle)
        else:
            pygame.draw.rect(screen, BACKGROUND_BOARD, self.rectangle)

    def highlight(self, screen, player, board):
        pygame.draw.rect(screen, player.colour_rgb, self.rectangle)
        self.draw_conditions(screen)
        if self.piece:
            board.draw_piece(self.piece)
        elif self.barrier:
            board.draw_barrier(self.barrier)

    def highlight_strong(self, screen, player, board):
        pygame.draw.rect(screen, player.colour_rgb_strong, self.rectangle)
        self.draw_conditions(screen)
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

            field = board.get_field(x, y)

            if field:
                adjacent.append(field)

        return adjacent

    def check_legal_movement(self, piece):
        if self.type == 'no field':
            return False
        elif self.occupied:
            return False
        elif self.type == 'temple square' and self.owner == piece.player:
            return False
        elif not self.permitted_area_condition(piece):
            return False

        return True

    def check_flame(self, piece):
        if self.flame:
            if piece.player in self.flame_casters and len(self.flame_casters) == 1:
                return False
            if piece.immune("Flame"):
                return False

            return True

        else:
            return False

    def permitted_area_condition(self, piece):
        if self.ocean and piece.gender == 'female' and not piece.immune('Ocean'):
            return False
        if self.drought and piece.gender == 'male' and not piece.immune('Drought'):
            return False
        if self.check_flame(piece):
            return False

        return True

    def get_legal_adjacent(self, board, piece):

        adjacent = []

        fields = self.get_adjacent(board, type=piece.movement_type)

        for field in fields:
            if field.check_legal_movement(piece):
                adjacent.append(field)

        return adjacent
