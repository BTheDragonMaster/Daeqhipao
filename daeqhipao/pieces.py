#!/usr/bin/env python

import os
import pygame

from daeqhipao.illegal_moves import *
from daeqhipao.style import *
from daeqhipao.powers import *
import images.symbols
import copy

SYMBOL_DIR = os.path.dirname(images.symbols.__file__)

class Pieces:
    def __init__(self, pieces):
        self.pieces = pieces
        self.active_pieces = []
        self.passive_pieces = []
        self.set_active_and_passive_pieces()

    def set_active_and_passive_pieces(self):
        self.active_pieces = []
        self.passive_pieces = []
        for piece in self.pieces:
            if piece.active:
                self.active_pieces.append(piece)
            else:
                self.passive_pieces.append(piece)

    def check_zaopeng(self, player):
        for piece in self.pieces:
            if piece.player == player:
                if piece.active:
                    return False

        return True

    def zaopeng(self, player):
        for piece in self.pieces:
            if piece.player == player:
                if not piece.oblivion:
                    piece.wake(self)
                else:
                    piece.countdown_oblivion()
        self.set_active_and_passive_pieces()


class Piece:
    def __init__(self, piece_id, player):
        self.id = piece_id
        self.location = None
        self.name = None
        self.gender = None
        
        self.active = True
        self.player = player

        self.idea = False
        self.illusion = False
        self.perception = 0
        self.legacy = False
        self.legacy_frequency = False
        self.legacy_duration = False
        
        self.union = False
        self.union_partners = set()
        self.communication = 0

        self.blindness = 0
        self.oblivion = 0
        self.liberation = 0

        self.ocean_fields = set()
        self.drought_fields = set()
        self.flame_fields = set()

        self.symbol_image = None

        self.piece_rectangle = None
        self.symbol_rectangle = None
        self.selection_nr = 0

        self.movement_type = 'all'


    def __eq__(self, piece):
        if type(self) == type(piece):
            if self.id == piece.id:
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):
        return self.id

    def __repr__(self):
        return self.name

    def get_movement_options(self, board):
        legal_fields = self.location.get_legal_adjacent(board, self)

        return legal_fields

    def set_piece_rectangle(self):
        x = (1 + self.location.x) * SQUARE_WIDTH + PIECE_PADDING
        y = (1 + self.location.y) * SQUARE_WIDTH + PIECE_PADDING
        self.piece_rectangle = pygame.Rect(x, y, PIECE_SIZE, PIECE_SIZE)

    def set_symbol_rectangle(self):
        x = (1 + self.location.x) * SQUARE_WIDTH + SYMBOL_PADDING
        y = (1 + self.location.y) * SQUARE_WIDTH + SYMBOL_PADDING
        self.symbol_rectangle = pygame.Rect(x, y, SYMBOL_SIZE, SYMBOL_SIZE)

    def load_symbol_image(self):
        symbol = os.path.join(SYMBOL_DIR, f'{self.name.lower()}.png')
        self.symbol_image = pygame.image.load(symbol)

    def set_location(self, location, board):
        x, y = location

        field = board.get_field(x, y)

        if field:
        
            self.location = field
            field.piece = self
            field.check_occupied()

        self.set_piece_rectangle()
        self.set_symbol_rectangle()

    def choose_legacy_effect(self, choice, power):
        assert self.legacy
        assert choice in ['duration', 'frequency']

        duration = {'Time', 'Mind', 'Perception', 'Union', 'Communication',
                    'Oblivion', 'Liberation', 'Blindness', 'Ocean', 'Flame',
                    'Drought', 'Void'}
        frequency = {'Illusion', 'Idea', 'Time', 'Life', 'Death', 'Wave',
                     'Perception', 'Union', 'Impression', 'Communication',
                     'Metamorphosis', 'Oblivion', 'Liberation', 'Blindness',
                     'Earth', 'Ocean', 'Sun', 'Sky', 'Quake', 'Wind', 'Shadow',
                     'Bloodmaker', 'Metalmaker', 'Fog', 'Drought', 'Void',
                     'End', 'Night'}
        

        if choice == 'duration':
            if not power in duration:
                raise IllegalPower('duration')
            self.legacy_duration = True
        elif choice == 'frequency':
            if not power in frequency:
                raise IllegalPower('frequency')
            self.legacy_frequency = True

    def clear_location(self, board):
        board.get_field(self.location).piece = None
        board.get_field(self.location).check_occupied()

        self.location = None

    def sleep(self, pieces):
        if not self.legacy_frequency:
            self.active = False
            pieces.active_pieces.remove(self)
            pieces.passive_pieces.append(self)
            if self.union:
                self.trigger_union(pieces, 'sleep')

    def wake(self, pieces):
        self.active = True
        for field in self.drought_fields:
            field.deactivate_drought(self)
        for field in self.ocean_fields:
            field.deactivate_ocean(self)
        self.ocean_fields = set()
        self.drought_fields = set()
        pieces.active_pieces.append(self)
        pieces.passive_pieces.remove(self)

        if self.union:
            self.trigger_union(pieces, 'wake')

    def set_perception(self, user):
        if user.legacy_duration:
            self.perception = 4
        else:
            self.perception = 2
    def countdown_perception(self):
        self.perception -= 1
        assert self.perception >= 0

    def activate_union(self, piece):
        self.union = True
        self.union_partners.add(piece)
        for piece_2 in piece.union_partners:
            if not piece_2 == self:
                self.union_partners.add(piece)

    def trigger_union(self, pieces, wake_or_sleep):

        self.union = False
        for union_partner in self.union_partners:
            union_partner.union = False
            union_partner.union_partners = set()
            if wake_or_sleep == 'wake':
                union_partner.wake(pieces)
            elif wake_or_sleep == 'sleep':
                union_partner.sleep(pieces)
        self.union_partners = set()

    def deactivate_legacy(self, choice):
        self.legacy_duration = False
        self.legacy_frequency = False
        self.legacy = False

    def set_communication(self, user):
        if user.legacy_duration:
            self.communication = 2
        else:
            self.communication = 1
    def countdown_communication(self):
        self.communication -= 1
        assert self.communication >= 0

    def activate_illusion(self):
        self.illusion = True
        self.player.illusion = True
        
    def deactivate_illusion(self):
        self.illusion = False
        self.player.illusion = False

    def activate_idea(self):
        self.idea = True
        self.player.idea = True
        
    def deactivate_idea(self):
        self.idea = False
        self.player.idea = False

    def set_blindness(self, user):
        if user.legacy_duration:
            self.blindness = 4
        else:
            self.blindness = 2
        
    def countdown_blindness(self):
        self.blindness -= 1
        assert self.blindness >= 0

    def set_oblivion(self, user):
        if user.legacy_duration:
            self.oblivion = 2
        else:
            self.oblivion = 1
    def countdown_oblivion(self):
        self.oblivion -= 1
        assert self.oblivion >= 0

    def set_liberation(self, user):
        if user.legacy_duration:
            self.liberation = 3
        else:
            self.liberation = 2
            
    def countdown_liberation(self):
        self.liberation -= 1
        assert self.liberation >= 0

    def immune(self, power):
        if self.perception:
            return True
        
        elif self.type == 'God':
            if power in [p.name for p in self.powers]:
                return True
            else:
                return False
        elif self.type == 'Heir':
            if power == self.name:
                return True
            else:
                return False

    def check_legal_move_movement(self, target_location, board):
        if not target_location in self.get_movement_options(board):
            raise IllegalMove('range')

    def check_legal_move_general(self, target_location, board):

        if target_location.ocean and self.gender == 'F' and not \
           self.immune('Ocean'):
                raise IllegalMove('ocean')

        elif target_location.drought and self.gender == 'M' and not \
             self.immune('Drought'):
            raise IllegalMove('drought')

        elif target_location.flame and self.player not in \
             target_location.flame_casters and not self.immune("Flame"):
            raise IllegalMove('flame')

        elif target_location.occupied:
            if target_location.piece:
                raise IllegalMove('piece')
            elif target_location.barrier:
                raise IllegalMove('barrier')

        elif target_location.type == "Temple" and \
             target_location.player == self.player:
            raise IllegalMove('temple')

    def move(self, target_location, board):
        print(self.name)
        original_x = self.location.x
        original_y = self.location.y


        x_diff = target_location.x - self.location.x
        y_diff = target_location.y - self.location.y

        self.location.piece = None
        self.location.check_occupied()
        
        self.location = target_location
        self.location.piece = self
        self.location.check_occupied()

        self.piece_rectangle = self.piece_rectangle.move(x_diff * SQUARE_WIDTH, y_diff * SQUARE_WIDTH)
        self.symbol_rectangle = self.symbol_rectangle.move(x_diff * SQUARE_WIDTH, y_diff * SQUARE_WIDTH)
        origin_square = board.get_field(original_x, original_y)

        board.redraw_field(origin_square, BACKGROUND_BOARD)
        board.draw_piece(self)

    def select_piece(self, piece, power):


        if piece.immune(power):
            raise Immune("%s is immune to the power %s." % (piece, power))


class God(Piece):
    def __init__(self, nr, player):
        Piece.__init__(self, nr, player)
        self.type = 'God'
        self.movement_type = 'all'

        
#==============================================================================

class Builder(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'female'
        self.name = "Builder"
        self.powers = [EarthPower(self), OceanPower(self), SkyPower(self), SunPower(self)]
        self.symbol = 'e'
        self.load_symbol_image()

class Alchemist(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'female'
        self.name = "Alchemist"
        self.powers = [MetalmakerPower(self), BloodmakerPower(self), FogPower(self), FlamePower(self)]
        self.symbol = 'g'
        self.load_symbol_image()

class Connector(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'female'
        self.name = "Connector"
        self.powers = [UnionPower(self), ImpressionPower(self), CommunicationPower(self), FamiliarityPower(self)]
        self.symbol = 'b'
        self.load_symbol_image()
        
class Wiper(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'female'
        self.name = 'Wiper'
        self.powers = [DeathPower(self), BlindnessPower(self), OblivionPower(self), LiberationPower(self)]
        self.symbol = 'd'
        self.load_symbol_image()

class Mover(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'male'
        self.name = 'Mover'
        self.powers = [QuakePower(self), WavePower(self), WindPower(self), ShadowPower(self)]
        self.symbol = 'f'
        self.load_symbol_image()

class Consumer(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'male'
        self.name = 'Consumer'
        self.powers = [VoidPower(self), DroughtPower(self), EndPower(self), NightPower(self)]
        self.symbol = 'h'
        self.load_symbol_image()

class Gifter(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'male'
        self.name = 'Gifter'
        self.powers = [LifePower(self), PerceptionPower(self), MindPower(self), LegacyPower(self)]
        self.symbol = 'a'
        self.load_symbol_image()

class Director(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'male'
        self.name = 'Director'
        self.powers = [TimePower(self), IllusionPower(self), IdeaPower(self), MetamorphosisPower(self)]
        self.symbol = 'c'
        self.load_symbol_image()

#==============================================================================

class FemaleHeir(Piece):
    def __init__(self, nr, player):
        Piece.__init__(self, nr, player)
        self.gender = 'female'
        self.type = 'Heir'
        self.movement_type = 'horizontal'

class MaleHeir(Piece):
    def __init__(self, nr, player):
        Piece.__init__(self, nr, player)
        self.gender = 'male'
        self.type = 'Heir'
        self.movement_type = 'diagonal'


#==============================================================================

class Union(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Union"
        self.symbol = 'm'
        self.load_symbol_image()
        self.power = UnionPower(self)


class Impression(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Impression"
        self.symbol = 'n'
        self.load_symbol_image()
        self.power = ImpressionPower(self)
        self.selections = ['piece']

    def use_power(self, piece, board):
        self.select_piece(piece, self.name)

        if board.get_field(piece.location).type == \
           "Temple Area":
            raise IllegalPower('impression')

        old_location = copy.copy(self.location)
        piece_location = copy.copy(piece.location)

        board.get_field(old_location).piece = piece
        board.get_field(piece_location).piece = self

        self.location = board.get_field(piece_location)
        piece.location = board.get_field(old_location)

        self.sleep()


class Communication(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Communication"
        self.symbol = 'o'
        self.load_symbol_image()
        self.selections = ['piece']
        self.power = CommunicationPower(self)

    def use_power(self, piece):
        self.select_piece(piece, self.name)

        self.activate_communication()

        self.sleep()

class Familiarity(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Familiarity"
        self.symbol = 'p'
        self.load_symbol_image()
        self.power = FamiliarityPower(self)

    def use_power(self, piece, pieces):
        raise NotImplementedError

class Death(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Death"
        self.symbol = 'u'
        self.load_symbol_image()
        self.power = DeathPower(self)

    def use_power(self, piece):
        self.select_piece(piece, self.name)

        if not piece.active:
            raise IllegalPower('death')

        piece.sleep()
        self.sleep()

class Blindness(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Blindness"
        self.symbol = 'v'
        self.load_symbol_image()
        self.power = BlindnessPower(self)

    def use_power(self, piece):
        self.select_piece(piece, self.name)

        piece.set_blindness(self)
        self.sleep()

class Oblivion(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Oblivion"
        self.symbol = 'w'
        self.load_symbol_image()
        self.selections = ['piece']
        self.power = OblivionPower(self)

    def use_power(self, piece):
        self.select_piece(piece, self.name)

        if not piece.passive:
            raise IllegalPower('oblivion')

        piece.set_oblivion(self)
        self.sleep()

class Liberation(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Liberation"
        self.symbol = 'x'
        self.load_symbol_image()
        self.selections = ['piece']
        self.power = LiberationPower(self)

    def use_power(self, piece):
        self.select_piece(piece, self.name)

        piece.set_liberation(self)
        self.sleep()


class Earth(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Earth"
        self.symbol = 'y'
        self.load_symbol_image()
        self.selections = ['field']
        self.power = EarthPower(self)

    def use_power(self, barriers, board, field_1, field_2=None):
        barriers.place_barrier(field_1, board)
        if field_2:
            barriers.place_barrier(field_2, board)

        self.sleep()

class Ocean(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Ocean"
        self.symbol = 'z'
        self.load_symbol_image()
        self.power = OceanPower(self)

    def use_power(self, field, board):
        board.check_field(field)
        adjacent_fields = field.get_adjacent(board)
        
        for field in adjacent_fields:
            field.ocean = True
            
        self.sleep()
        

class Sky(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Sky"
        self.symbol = 'A'
        self.load_symbol_image()
        self.power = SkyPower(self)

    def use_power(self, piece, board):
        self.select_piece(piece, self.name)

        adjacent = self.location.check_adjacent(piece.location, board)

        if not adjacent:
            raise IllegalPower('sky')

        assert not (0 == diff_x == diff_y)

        if self.location.x > piece.location.x:
            new_x = piece.location.x - 1
        elif self.location.x == piece.location.x:
            new_x = self.location.x
        else:
            new_x = piece.location.x + 1

        if self.location.y > piece.location.y:
            new_y = piece.location.y - 1
        elif self.location.y == piece.location.y:
            new_y = self.location.y
        else:
            new_y = piece.location.y + 1

        new_field = PhantomField(new_x, new_y)
        board.check_field(new_field)
        new_field = board.get_field(new_field)
        
        self.check_legal_move_general(new_field, board)
        self.move(new_field, board)

        self.sleep()
        

class Sun(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Sun"
        self.symbol = 'B'
        self.load_symbol_image()
        self.power = SunPower(self)

    def use_power(self, field, board):
        legal_locations = self.find_legal_locations(field, board)
        legal_locations = self.filter_legal_locations(legal_locations,
                                                       board)

        if not field in legal_locations:
            raise IllegalPower('sun')

        self.move(field, board)

        self.sleep()

    def find_legal_locations(self, field, board):

        legal_locations = set([])

        for i in range(self.location.x - 2, self.location.x + 3):
            for j in range(self.location.y - 2, self.location.y + 3):

                if self.location.x == i and self.location.y == j:
                    continue
                elif self.location.x != i and self.location.y != j:
                    continue
                else:
                    legal_locations.add(PhantomField(i, j))

        return legal_locations
    

    def filter_legal_locations(self, legal_locations, board):
        filtered_locations = []
        
        direction_1 = []
        direction_2 = []
        direction_3 = []
        direction_4 = []

        for location in legal_locations:
            if self.location.y > location.y:
                direction_1.append(location)
            elif self.location.x > location.x:
                direction_2.append(location)
            elif self.location.y < location.y:
                direction_3.append(location)
            elif self.location.x < location.x:
                direction_4.append(location)

        direction_1.sort(key= lambda field: field.y, reverse=True)
        direction_2.sort(key= lambda field: field.x, reverse=True)
        direction_3.sort(key= lambda field: field.y)
        direction_4.sort(key= lambda field: field.x)

        all_directions = [direction_1, direction_2, direction_3, direction_4]

        for direction in all_directions:
            for field in direction:
                try:
                    board.check_field(field)
                    self.check_legal_move_general(board.get_field(field), board)
                    filtered_locations.append(field)
                except (IllegalMove, IllegalField):
                    break

        return filtered_locations
            

class Metalmaker(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Metalmaker"
        self.symbol = 'G'
        self.load_symbol_image()
        self.power = MetalmakerPower(self)

    def use_power(self, field, barriers, board):
        
        if barriers.count == 3:
            raise IllegalPower('metalmaker')

        board.check_field(field)
        self.check_legal_move_movement(field, board)
        self.check_legal_move_general(field, board)

        old_field = self.location

        self.move(old_field, board)
        barriers.place_barrier(field, board)

        self.sleep()

class Bloodmaker(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Bloodmaker"
        self.symbol = 'H'
        self.load_symbol_image()
        self.power = BloodmakerPower(self)

    def use_power(self, piece, barrier_field, barriers, board):
        self.select_piece(piece, self.name)
        
        if not board.get_field(barrier_field).barrier:
            raise IllegalBarrier('no barrier')
        
        if not piece.location.check_adjacent(barrier_field, board):
            raise IllegalPower('bloodmaker')

        board.get_field(barrier_field).occupied = False

        piece_location = copy.copy(piece.location)

        piece.move(barrier_field, board)
        barriers.move_barrier(barrier_field, piece_location)

        self.sleep()

class Fog(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Fog"
        self.symbol = 'I'
        self.load_symbol_image()
        self.power = FogPower(self)

    def use_power(self, piece_1, piece_2, board):
        self.select_piece(piece_1, self.name)
        self.select_piece(piece_2, self.name)

        if not piece_1.location.check_adjacent(piece_2.location, board):
            raise IllegalPower('fog')

        piece1_location = copy.copy(piece_1.location)
        piece2_location = copy.copy(piece_2.location)

        board.get_field(piece1_location).piece = piece_2
        board.get_field(piece2_location).piece = piece_1

        piece_1.location = board.get_field(piece2_location)
        piece_2.location = board.get_field(piece1_location)

        self.sleep()

class Flame(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Flame"
        self.symbol = 'J'
        self.load_symbol_image()
        self.power = FlamePower(self)

    def use_power(self, board):
        for field in board.find_flame_locations():
            board.get_field(field).activate_flame(self)

        self.sleep()


    def find_flame_locations(self, board):

        flame_locations = set(self.location.get_adjacent(board))

        for i in range(self.location.x - 2, self.location.x + 3):
            for j in range(self.location.y - 2, self.location.y + 3):

                if self.location.x == i and self.location.y == j:
                    continue
                elif self.location.x != i and self.location.y != j:
                    continue
                else:
                    try:
                        board.check_field(PhantomField(i, j))
                        flame_locations.add(PhantomField(i, j))
                    except IllegalField:
                        pass
                    
        return flame_locations
        


#==============================================================================

class Life(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Life"
        self.symbol = 'i'
        self.load_symbol_image()
        self.power = LifePower(self)

    def use_power(self, piece):
        self.select_piece(piece, self.name)
        if piece.active:
            raise IllegalPower('life')

        piece.active = True
        self.sleep()

class Perception(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Perception"
        self.symbol = 'j'
        self.load_symbol_image()
        self.power = PerceptionPower(self)

    def use_power(self, piece):
        self.select_piece(piece, self.name)

        piece.set_perception(self)
        self.sleep()

class Mind(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Mind"
        self.symbol = 'k'
        self.load_symbol_image()
        self.power = MindPower(self)

    def use_power(self, board):
        temple = board.get_field(self.player.temple)
        temple.set_mind(self)

        self.sleep()

class Legacy(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Legacy"
        self.symbol = 'l'
        self.load_symbol_image()
        self.power = LegacyPower(self)

    def use_power(self, piece):
        self.select_piece(piece, self.name)
        if piece.legacy:
            raise IllegalPower('legacy')

        piece.legacy = True
        self.sleep()

class Time(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Time"
        self.symbol = 'q'
        self.load_symbol_image()
        self.power = TimePower(self)

    def use_power(self, player):
        
        player.set_time_pieces(self)
        player.set_time_count()
        self.sleep()
        

class Illusion(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Illusion"
        self.symbol = 'r'
        self.load_symbol_image()
        self.power = IllusionPower(self)

    def use_power(self, piece):

        self.select_piece(piece, self.name)

        piece.player.add_piece_illusion(piece)
        self.sleep()
        

class Idea(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Idea"
        self.symbol = 's'
        self.load_symbol_image()
        self.power = IdeaPower(self)

    def use_power(self, piece):
        self.select_piece(piece, self.name)
        piece.player.add_piece_idea(piece)
        self.sleep()
        

class Metamorphosis(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Metamorphosis"
        self.symbol = 't'
        self.load_symbol_image()
        self.power = MetamorphosisPower(self)

    def use_power(self, piece_1, piece_2, board, players):
        if piece_1.player == self.player:
            raise IllegalPower('metamorphosis')

        if piece_2.player == self.player:
            raise IllegalPower('metamorphosis')

        if piece_1.type == 'God':
            raise IllegalPower('god')

        if piece_2.type == 'God':
            raise IllegalPower('god')

        player_1 = copy.copy(piece_1.player)
        player_2 = copy.copy(piece_2.player)

        piece1_location = copy.copy(piece_1.location)
        piece2_location = copy.copy(piece_2.location)

        board.get_field(piece1_location).piece = piece_2
        board.get_field(piece2_location).piece = piece_1

        piece_1.location = board.get_field(piece2_location)
        piece_2.location = board.get_field(piece1_location)


class Quake(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, location, player)
        self.name = "Quake"
        self.symbol = 'C'
        self.load_symbol_image()
        self.power = QuakePower(self)


class Wave(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Wave"
        self.symbol = 'D'
        self.load_symbol_image()
        self.power = WavePower(self)


class Wind(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Wind"
        self.symbol = 'E'
        self.load_symbol_image()
        self.power = WindPower(self)


class Shadow(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Shadow"
        self.symbol = 'F'
        self.load_symbol_image()
        self.power = ShadowPower(self)


class Void(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Void"
        self.symbol = 'K'
        self.load_symbol_image()
        self.power = VoidPower(self)


class Drought(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Drought"
        self.symbol = 'L'
        self.load_symbol_image()
        self.power = DroughtPower(self)


class End(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "End"
        self.symbol = 'M'
        self.load_symbol_image()
        self.power = EndPower(self)



class Night(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Night"
        self.symbol = 'N'
        self.load_symbol_image()
        self.power = NightPower(self)
