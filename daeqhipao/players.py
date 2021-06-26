#!/usr/bin/env python

from pieces import *

class Plsyers():
    def __init__(self, players):
        self.players = {}
        for player in players:
            self.players[player.id] = player

    def get_player(self, player_id):
        return self.players[player_id]
        

class Player():
    colours = {1: 'red',
               2: 'orange',
               3: 'blue',
               4: 'purple'}

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
        if player_id < 1 or player_id > 4:
            raise PlayerError('illegal number')
        self.id = player_id
        self.colour = self.colours[self.id]
        self.heirs = []
        self.god = None
        
        self.idea = []
        self.illusion = []
        self.time = 0
        self.time_pieces = 0

        self.temple = board.get_temple_square(self)
        
        self.free_positions = {1, 2, 3, 4, 5}

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
        all_pieces = self.heirs.append(self.god)
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
        piece = self.piece_dict[piece_name](piece_id, self)

        if not piece.type == 'Heir':
            raise IllegalPiece('no heir')

        self.heirs.append(piece)
        

    def assign_location(self, piece, location, board):
        if not 1 <= location <= 5:
            raise IllegalField('no starter')
        
        if not location in free_positions:
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
        
        

    
