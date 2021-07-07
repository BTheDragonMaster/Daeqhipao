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
        self.set_domains()
        self.set_god_groups()

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
                if not piece.active:
                    if not piece.oblivion:
                        piece.wake(self)
                    else:
                        piece.countdown_oblivion()
        self.set_active_and_passive_pieces()

    def get_pieces_player(self, player):
        player_pieces = []
        for piece in self.pieces:
            if piece.player == player:
                player_pieces.append(piece)

        return player_pieces

    def set_domains(self):
        self.spiritual_pieces = []
        self.physical_pieces = []
        for piece in self.pieces:
            if piece.domain == 'spiritual':
                self.spiritual_pieces.append(piece)
            elif piece.domain == 'physical':
                self.physical_pieces.append(piece)

    def set_god_groups(self):
        self.god_groups = {'builder': [],
                           'mover': [],
                           'alchemist': [],
                           'consumer': [],
                           'gifter': [],
                           'connector': [],
                           'director': [],
                           'wiper': []}
        for piece in self.pieces:
            if piece.god_group:
                self.god_groups[piece.god_group].append(piece)


class Piece:
    def __init__(self, piece_id, player):
        self.id = piece_id
        self.location = None
        self.name = None
        self.gender = None
        self.domain = None
        self.god_group = None
        
        self.active = True
        self.player = player

        self.idea = False
        self.illusion = False
        self.perception = 0
        self.legacy = False
        self.legacy_frequency = False
        self.legacy_duration = False

        self.potency = False
        self.frequency = False
        
        self.union = False
        self.union_partners = set()
        self.communication = 0
        self.communication_active = 0

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
        self.perception = 0

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

    def is_last_active_piece(self, pieces):
        if self.active:
            active_count = 0
            for piece in pieces.get_pieces_player(self.player):
                if piece.active:
                    active_count += 1

            if active_count == 1:
                return True
            else:
                return False
        else:
            return False

    def countdown_frequency(self):
        if self.frequency > 0:
            self.frequency -= 1

    def countdown_potency(self):
        if self.potency > 0:
            self.potency -= 1

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

    def set_potency(self, user):
        if self.player == user.player:
            self.potency = 2
        else:
            self.potency = 1

    def set_frequency(self, user):
        if self.player == user.player:
            self.frequency = 2
        else:
            self.frequency = 1

    def activate_perception(self, user, potency=0):
        if not potency:
            if self.player == user.player:
                self.perception = 3
            else:
                self.perception = 2
        else:
            if self.player == user.player:
                self.perception = 5
            else:
                self.perception = 4

    def countdown_perception(self):
        if self.perception:
            self.perception -= 1

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



    def activate_communication(self, user, potency=0):

        if self.player == user.player:
            self.communication_active = 2
        else:
            self.communication_active = 1

        if not potency:
            self.communication = 2
        else:
            self.communication = 4

    def countdown_communication(self):
        if self.communication > 1:
            self.communication -= 1

    def reset_communication(self):
        if self.communication_active > 0:
            self.communication_active -= 1

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
        if self.blindness > 0:
            self.blindness -= 1

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
        if self.liberation > 0:
            self.liberation -= 1

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

    def move(self, target_location, board):
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
        self.domain = 'physical'

class Alchemist(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'female'
        self.name = "Alchemist"
        self.powers = [MetalmakerPower(self), BloodmakerPower(self), FogPower(self), FlamePower(self)]
        self.symbol = 'g'
        self.load_symbol_image()
        self.domain = 'physical'

class Connector(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'female'
        self.name = "Connector"
        self.powers = [UnionPower(self), ImpressionPower(self), CommunicationPower(self), FamiliarityPower(self)]
        self.symbol = 'b'
        self.load_symbol_image()
        self.domain = 'spiritual'

        
class Wiper(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'female'
        self.name = 'Wiper'
        self.powers = [DeathPower(self), BlindnessPower(self), OblivionPower(self), LiberationPower(self)]
        self.symbol = 'd'
        self.load_symbol_image()
        self.domain = 'spiritual'

class Mover(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'male'
        self.name = 'Mover'
        self.powers = [QuakePower(self), WavePower(self), WindPower(self), ShadowPower(self)]
        self.symbol = 'f'
        self.load_symbol_image()
        self.domain = 'physical'

class Consumer(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'male'
        self.name = 'Consumer'
        self.powers = [VoidPower(self), DroughtPower(self), EndPower(self), NightPower(self)]
        self.symbol = 'h'
        self.load_symbol_image()
        self.domain = 'physical'

class Gifter(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'male'
        self.name = 'Gifter'
        self.powers = [LifePower(self), PerceptionPower(self), MindPower(self), LegacyPower(self)]
        self.symbol = 'a'
        self.load_symbol_image()
        self.domain = 'spiritual'

class Director(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'male'
        self.name = 'Director'
        self.powers = [TimePower(self), IllusionPower(self), IdeaPower(self), MetamorphosisPower(self)]
        self.symbol = 'c'
        self.load_symbol_image()
        self.domain = 'spiritual'

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
        self.domain = 'spiritual'
        self.god_group = 'connector'


class Impression(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Impression"
        self.symbol = 'n'
        self.load_symbol_image()
        self.power = ImpressionPower(self)
        self.domain = 'spiritual'
        self.god_group = 'connector'


class Communication(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Communication"
        self.symbol = 'o'
        self.load_symbol_image()
        self.selections = ['piece']
        self.power = CommunicationPower(self)
        self.domain = 'spiritual'
        self.god_group = 'connector'

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
        self.domain = 'spiritual'
        self.god_group = 'connector'

    def use_power(self, piece, pieces):
        raise NotImplementedError


class Death(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Death"
        self.symbol = 'u'
        self.load_symbol_image()
        self.power = DeathPower(self)
        self.domain = 'spiritual'
        self.god_group = 'wiper'

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
        self.domain = 'spiritual'
        self.god_group = 'wiper'

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
        self.domain = 'spiritual'
        self.god_group = 'wiper'

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
        self.domain = 'spiritual'
        self.god_group = 'wiper'

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
        self.domain = 'physical'
        self.god_group = 'builder'


class Ocean(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Ocean"
        self.symbol = 'z'
        self.load_symbol_image()
        self.power = OceanPower(self)
        self.domain = 'physical'
        self.god_group = 'builder'


class Sky(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Sky"
        self.symbol = 'A'
        self.load_symbol_image()
        self.power = SkyPower(self)
        self.domain = 'physical'
        self.god_group = 'builder'


class Sun(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Sun"
        self.symbol = 'B'
        self.load_symbol_image()
        self.power = SunPower(self)
        self.domain = 'physical'
        self.god_group = 'builder'
            

class Metalmaker(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Metalmaker"
        self.symbol = 'G'
        self.load_symbol_image()
        self.power = MetalmakerPower(self)
        self.domain = 'physical'
        self.god_group = 'alchemist'


class Bloodmaker(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Bloodmaker"
        self.symbol = 'H'
        self.load_symbol_image()
        self.power = BloodmakerPower(self)
        self.domain = 'physical'
        self.god_group = 'alchemist'


class Fog(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Fog"
        self.symbol = 'I'
        self.load_symbol_image()
        self.power = FogPower(self)
        self.domain = 'physical'
        self.god_group = 'alchemist'


class Flame(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Flame"
        self.symbol = 'J'
        self.load_symbol_image()
        self.power = FlamePower(self)
        self.domain = 'physical'
        self.god_group = 'alchemist'


#==============================================================================

class Life(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Life"
        self.symbol = 'i'
        self.load_symbol_image()
        self.power = LifePower(self)
        self.domain = 'spiritual'
        self.god_group = 'gifter'


class Perception(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Perception"
        self.symbol = 'j'
        self.load_symbol_image()
        self.power = PerceptionPower(self)
        self.domain = 'spiritual'
        self.god_group = 'gifter'


class Mind(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Mind"
        self.symbol = 'k'
        self.load_symbol_image()
        self.power = MindPower(self)
        self.domain = 'spiritual'
        self.god_group = 'gifter'


class Legacy(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Legacy"
        self.symbol = 'l'
        self.load_symbol_image()
        self.power = LegacyPower(self)
        self.domain = 'spiritual'
        self.god_group = 'gifter'

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
        self.domain = 'spiritual'
        self.god_group = 'director'


class Illusion(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Illusion"
        self.symbol = 'r'
        self.load_symbol_image()
        self.power = IllusionPower(self)
        self.domain = 'spiritual'
        self.god_group = 'director'


class Idea(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Idea"
        self.symbol = 's'
        self.load_symbol_image()
        self.power = IdeaPower(self)
        self.domain = 'spiritual'
        self.god_group = 'director'


class Metamorphosis(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Metamorphosis"
        self.symbol = 't'
        self.load_symbol_image()
        self.power = MetamorphosisPower(self)
        self.domain = 'spiritual'
        self.god_group = 'director'

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
        MaleHeir.__init__(self, nr, player)
        self.name = "Quake"
        self.symbol = 'C'
        self.load_symbol_image()
        self.power = QuakePower(self)
        self.domain = 'physical'
        self.god_group = 'mover'


class Wave(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Wave"
        self.symbol = 'D'
        self.load_symbol_image()
        self.power = WavePower(self)
        self.domain = 'physical'
        self.god_group = 'mover'


class Wind(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Wind"
        self.symbol = 'E'
        self.load_symbol_image()
        self.power = WindPower(self)
        self.domain = 'physical'
        self.god_group = 'mover'


class Shadow(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Shadow"
        self.symbol = 'F'
        self.load_symbol_image()
        self.power = ShadowPower(self)
        self.domain = 'physical'
        self.god_group = 'mover'


class Void(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Void"
        self.symbol = 'K'
        self.load_symbol_image()
        self.power = VoidPower(self)
        self.domain = 'physical'
        self.god_group = 'consumer'


class Drought(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Drought"
        self.symbol = 'L'
        self.load_symbol_image()
        self.power = DroughtPower(self)
        self.domain = 'physical'
        self.god_group = 'consumer'


class End(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "End"
        self.symbol = 'M'
        self.load_symbol_image()
        self.power = EndPower(self)
        self.domain = 'physical'
        self.god_group = 'consumer'


class Night(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Night"
        self.symbol = 'N'
        self.load_symbol_image()
        self.power = NightPower(self)
        self.domain = 'physical'
        self.god_group = 'consumer'
