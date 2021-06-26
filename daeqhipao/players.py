#!/usr/bin/env python

from daeqhipao.pieces import *
from daeqhipao.illegal_moves import *

class PlayerProperties:
    player_to_colour = {1: (165, 30, 30),
                        2: (236, 126, 0),
                        3: (67, 84, 198),
                        4: (152, 46, 191)}
    player_to_starting_squares = {1: [(3, 9), (4, 9), (5, 9), (6, 9), (7, 9)],
                                  2: [(1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],
                                  3: [(3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
                                  4: [(9, 3), (9, 4), (9, 5), (9, 6), (9, 7)]}

    player_to_temple_area = {1: [(3, 8), (4, 8), (5, 8), (6, 8), (7, 8)],
                             2: [(2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],
                             3: [(3, 2), (4, 2), (5, 2), (6, 2), (7, 2)],
                             4: [(8, 3), (8, 4), (8, 5), (8, 6), (8, 7)]}

    player_to_temple_square = {1: (5, 10),
                               2: (0, 5),
                               3: (5, 0),
                               4: (10, 5)}

PLAYER_PROPERTIES = PlayerProperties()

class Players:
    def __init__(self, players):
        self.players = {}
        for player in players:
            self.players[player.id] = player

    def get_player(self, player_id):
        return self.players[player_id]
        

class Player:


    piece_dict = {"Gifter": Gifter,
                  "Connector": Connector,
                  "Director": Director,
                  "Wiper": Wiper,
                  "Builder": Builder,
                  "Mover": Mover,
                  "Alchemist": Alchemist,
                  "Consumer": Consumer,
                  "Life": Life,
                  "Perception": Perception,
                  "Mind": Mind,
                  "Legacy": Legacy,
                  "Union": Union,
                  "Impression": Impression,
                  "Communication": Communication,
                  "Familiarity": Familiarity,
                  "Time": Time,
                  "Illusion": Illusion,
                  "Idea": Idea,
                  "Metamorphosis": Metamorphosis,
                  "Death": Death,
                  "Blindness": Blindness,
                  "Oblivion": Oblivion,
                  "Liberation": Liberation,
                  "Earth": Earth,
                  "Ocean": Ocean,
                  "Sky": Sky,
                  "Sun": Sun,
                  "Quake": Quake,
                  "Wave": Wave,
                  "Wind": Wind,
                  "Shadow": Shadow,
                  "Metalmaker": Metalmaker,
                  "Bloodmaker": Bloodmaker,
                  "Fog": Fog,
                  "Flame": Flame,
                  "Void": Void,
                  "Drought": Drought,
                  "End": End,
                  "Night": Night}


    def __init__(self, player_id, board):
        if not type(player_id) == int or player_id < 1 or player_id > 4:
            raise PlayerError('illegal number')
        self.id = player_id
        self.colour = PLAYER_PROPERTIES.player_to_colour[self.id]
        self.heirs = []
        self.god = None
        self.name = None
        
        self.idea = []
        self.illusion = []
        self.time = 0
        self.time_pieces = 0

        self.temple = PLAYER_PROPERTIES.player_to_temple_square[self.id]
        self.starting_squares = PLAYER_PROPERTIES.player_to_starting_squares[self.id]
        self.temple_area = PLAYER_PROPERTIES.player_to_temple_area[self.id]
        
        self.free_positions = {1, 2, 3, 4, 5}

    def __eq__(self, player):
        return self.id == player.id

    def __hash__(self):
        return self.id

    def __repr__(self):
        if self.name:
            return self.name
        else:
            return f"Player {self.id}"

    def set_name(self, name):
        self.name = name

    def set_time_pieces(self, user):
        if user.legacy_duration:
            self.time_pieces = 3
        else:
            self.time_pieces = 2

    def add_piece_idea(self, piece):
        self.idea.append(piece)

    def remove_piece_idea(self, piece):
        assert self.illusion[0] == piece
        self.idea.remove(piece)

    def add_piece_illusion(self, piece):
        self.illusion.append(piece)

    def remove_illusion_idea(self, piece):
        assert self.illusion[0] == piece
        self.illusion.remove(piece)

    def set_time_count(self):
        self.time += 1

    def deactivate_time(self):
        self.time -= 0
        self.time_pieces = 0
        assert self.time >= 0

    def get_all_pieces(self):
        all_pieces = self.heirs + [self.god]
        return all_pieces

    def set_god(self, piece_name):
        piece_id = (self.id - 1) * 5 + 1
        piece = self.piece_dict[piece_name](piece_id, self)
        if not piece.type == 'God':
            raise IllegalPiece('no god')

        self.god = piece

    def set_heir(self, piece_name):

        heir_nr = len(self.heirs) + 1
        if heir_nr > 4:
            raise IllegalPiece('heirs')

        heir_id = (self.id - 1) * 5 + 1 + heir_nr
        piece = self.piece_dict[piece_name](heir_id, self)

        if not piece.type == 'Heir':
            raise IllegalPiece('no heir')

        self.heirs.append(piece)

    def set_field_ownership(self, board):
        x, y = self.temple
        board[x][y].set_ownership(self)

        for x, y in self.starting_squares:
            board[x][y].set_ownership(self)

        for x, y in self.temple_area:
            board[x][y].set_ownership(self)


    def assign_location(self, piece, location, board):
        if not 1 <= location <= 5:
            raise IllegalField('no starter')
        
        if not location in self.free_positions:
            raise IllegalField('occupied')

        field = board.get_starting_positions(self)[location]
        
        piece.set_location(field, board)

        self.free_positions.remove(location)

    def clear_all_locations(self, board):
        for piece in self.get_all_pieces():
            piece.clear_location(board)
        
    def clear_location(self, piece, board):
        if not piece in self.get_all_pieces():
            raise IllegalPiece('not yours')
        piece.clear_location(board)
        
        

    
