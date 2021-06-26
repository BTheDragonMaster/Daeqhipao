#!/usr/bin/env python

from pieces import *
from board import *
from illegal_moves import *
from players import *
from PIL import ImageDraw, ImageFont, Image, ImageTk
#import tkinter as tkinter

daeqhipao_pieces = []




class DrawBoard():
    def __init__(self, board):
        self.board = board
        self.image = Image.new('RGB', (1300, 1300), color = 'white')
        self.font = ImageFont.truetype("Daeqhipao_v1_mac.ttf", 80)
        self.draw = ImageDraw.Draw(self.image)
        self.logo = Image.open("logo.png")
        

    def draw_frame(self):
        self.draw.line((600, 100, 700, 100), fill = (0,0,0))
        self.draw.line((400, 200, 900, 200), fill = (0,0,0))
        self.draw.line((400, 300, 900, 300), fill = (0,0,0))
        self.draw.line((200, 400, 1100, 400), fill = (0,0,0))
        self.draw.line((200, 500, 1100, 500), fill = (0,0,0))
        self.draw.line((100, 600, 1200, 600), fill = (0,0,0))
        self.draw.line((100, 700, 1200, 700), fill = (0,0,0))
        self.draw.line((200, 800, 1100, 800), fill = (0,0,0))
        self.draw.line((200, 900, 1100, 900), fill = (0,0,0))
        self.draw.line((400, 1000, 900, 1000), fill = (0,0,0))
        self.draw.line((400, 1100, 900, 1100), fill = (0,0,0))
        self.draw.line((600, 1200, 700, 1200), fill = (0,0,0))

        self.draw.line((100, 600, 100, 700), fill = (0,0,0))
        self.draw.line((200, 400, 200, 900), fill = (0,0,0))
        self.draw.line((300, 400, 300, 900), fill = (0,0,0))
        self.draw.line((400, 200, 400, 1100), fill = (0,0,0))
        self.draw.line((500, 200, 500, 1100), fill = (0,0,0))
        self.draw.line((600, 100, 600, 1200), fill = (0,0,0))
        self.draw.line((700, 100, 700, 1200), fill = (0,0,0))
        self.draw.line((800, 200, 800, 1100), fill = (0,0,0))
        self.draw.line((900, 200, 900, 1100), fill = (0,0,0))
        self.draw.line((1000, 400, 1000, 900), fill = (0,0,0))
        self.draw.line((1100, 400, 1100, 900), fill = (0,0,0))
        self.draw.line((1200, 600, 1200, 700), fill = (0,0,0))

        self.image.paste(self.logo, box = (600, 600))

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
            piece_body_dir = 'pieces/%s_passive.png' % piece.player.colour
        else:
            piece_body_dir = 'pieces/%s_%s_%s.png' % (piece.player.colour,
                                                      gender, piece_type)
        
        piece_image = Image.open(piece_body_dir)
        x_offset, y_offset = self.calc_offset(piece.location)
        self.image.paste(piece_image, box = (x_offset, y_offset))
        
        piece_symbol_dir = 'symbols/%s.png' % piece.name
        symbol_image = Image.open(piece_symbol_dir)
        x_offset, y_offset = self.calc_symbol_offset(x_offset, y_offset)
        self.image.paste(symbol_image, box = (x_offset, y_offset), mask=symbol_image)

    def draw_pieces(self, board):
        for row in board.board:
            for column in row:
                if column.piece:
                    self.draw_piece(column.piece)
    def draw_board(self, board):
        self.draw_frame()
        self.draw_pieces(board)

    def save_board(self):
        self.image.save("board.png")

    def show_board(self):
        self.image.show()

if __name__ == "__main__":
    board = Board()
    board_drawer = DrawBoard(board)
    board_drawer.draw_frame()
    board_drawer.save_board()
    player_1 = Player(1, board)
    player_3 = Player(3, board)
    player_2 = Player(2, board)
    
    
    sun = Sun(1, player_1)
    sun.set_location(board.get_field(Field(5, 1)), board)
    sky = Sky(2, player_1)
    sky.set_location(board.get_field(Field(4,1)), board)
    metalmaker = Metalmaker(3, player_1)
    metalmaker.set_location(board.get_field(Field(3, 1)), board)
    earth = Earth(4, player_1)
    earth.set_location(board.get_field(Field(6,1)), board)
    mover = Mover(5, player_1)
    mover.set_location(board.get_field(Field(7,1)), board)
    
    gifter = Gifter(6, player_3)
    gifter.set_location(board.get_field(Field(5,9)), board)
    death = Death(7, player_3)
    death.set_location(board.get_field(Field(3,9)), board)
    impression = Impression(8, player_3)
    impression.set_location(board.get_field(Field(4,9)), board)
    ocean = Ocean(9, player_3)
    ocean.set_location(board.get_field(Field(6,9)), board)
    bloodmaker = Bloodmaker(10, player_3)
    bloodmaker.set_location(board.get_field(Field(7,9)), board)
    
    #root.mainloop()
    board_drawer.draw_board(board)
    board_drawer.show_board()
    try:
        sun.use_power(Field(5,3), board)
    except Exception as e:
        print(e.message)

    board_drawer.draw_board(board)

    board_drawer.show_board()

    try:
        impression.use_power(sun, board)
    except Exception as e:
        print(e.message)
    board_drawer.draw_board(board)
    board_drawer.show_board()
    
    
    
