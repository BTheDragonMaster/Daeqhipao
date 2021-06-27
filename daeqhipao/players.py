#!/usr/bin/env python

from daeqhipao.pieces import *
from daeqhipao.illegal_moves import *
from daeqhipao.player_properties import PLAYER_PROPERTIES


class Players:
    def __init__(self, players):
        self.players = {}
        for player in players:
            self.players[player.id] = player

    def get_player(self, player_id):
        return self.players[player_id]
        

class Player:

    def __init__(self, player_id):
        if not type(player_id) == int or player_id < 1 or player_id > 4:
            raise PlayerError('illegal number')
        self.id = player_id
        self.colour = PLAYER_PROPERTIES.player_to_colour[self.id]
        self.colour_rgb = PLAYER_PROPERTIES.player_to_colour_rgb[self.id]
        self.colour_rgb_strong = PLAYER_PROPERTIES.player_to_colour_rgb_strong[self.id]
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
        board.board[x][y].set_ownership(self)

        for x, y in self.starting_squares:
            board.board[x][y].set_ownership(self)

        for x, y in self.temple_area:
            board.board[x][y].set_ownership(self)


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
        
        

    
