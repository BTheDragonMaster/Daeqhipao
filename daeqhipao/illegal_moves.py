class Immune(Exception):
    pass

class PlayerError(Exception):
    def __init__(self, reason):
        if reason == 'illegal number':
            self.message = "Player ID must be 1, 2, 3 or 4!"

class IllegalField(Exception):
    def __init__(self, reason):
        if reason == 'no field':
            self.message = "You selected a field that does not exist!"
        elif reason == 'occupied':
            self.message = "This location is already occupied!"
        elif reason == 'no starter':
            self.message = "This is not a starter square!"

class IllegalPiece(Exception):
    def __init__(self, reason):
        if reason == 'no god':
            self.message = "This is not a god piece! Please select a god."
        elif reason == 'heirs':
            self.message = "Can't select more than four heir pieces!"
        elif reason == 'no heir':
            self.message = "This is not an heir piece! Please select an heir."
        elif reason == 'not yours':
            self.message = "This is not one of your pieces!"
class IllegalMove(Exception):
    def __init__(self, reason):
        if reason == 'board':
            self.message = "This field does not exist!"
        elif reason == 'range':
            self.message = "Cannot reach this field!"
        elif reason == 'ocean':
            self.message = "Female pieces cannot set foot in the ocean!"
        elif reason == 'drought':
            self.message = "Male pieces cannot set foot in the desert!"
        elif reason == 'flame':
            self.message = "A fire rages in this field! You cannot move here!"
        elif reason == 'barrier':
            self.message = "This field is occupied by a barrier. You cannot move here!"
        elif reason == 'piece':
            self.message = "This field is occpied by another piece. You cannot move here!"
        elif reason == 'temple':
            self.message = "You cannot enter your own temple!"
        elif reason == 'illusion':
            self.message = "Can only force an active piece to move!"
        elif reason == 'idea':
            self.message = "Can only force an active piece to use its power!"
            

class IllegalPower(Exception):
    def __init__(self, reason):
        if reason == 'impression':
            self.message = "Cannot switch places with a piece in a temple area!"
        elif reason == 'death':
            self.message = "Piece is already dead!"
        elif reason == 'oblivion':
            self.message = "Only passive pieces are affected by this power!"
        elif reason == 'sky':
            self.message = "Piece out of range! Cannot jump!"
        elif reason == 'sun':
            self.message = "You cannot move to that square!"
        elif reason == 'metalmaker':
            self.message = "Already 3 barriers on the board! Cannot use your power."
        elif reason == 'bloodmaker':
            self.message = "This barrier is not adjacent!"
        elif reason == 'fog':
            self.message = "These two pieces are not adjacent to one another!"
        elif reason == 'union':
            self.message = "The two selected pieces must be in the same flip state!"
        elif reason == 'life':
            self.message = "This piece is already alive!"
        elif reason == 'duration':
            self.message = "The duration of this power cannot be altered!"
        elif reason == 'frequency':
            self.message = "The frequency of this power cannot be altered!"
        elif reason == 'metamorphosis':
            self.message = "You cannot use metamorphosis on pieces you own yourself!"
        elif reason == 'god':
            self.message = "You cannot use metamorphosis on god pieces!"

            
class IllegalBarrier(Exception):
    def __init__(self, reason):
        if reason == 'occupied':
            self.message = "This square is already occupied."
        if reason == 'count':
            self.message = "There are already three barriers on the board!"
        if reason == 'none':
            self.message = "There are no barriers on the board to remove!"
        if reason == 'no barrier':
            self.message = "There is no barrier occupying this square!"
        if reason == 'temple':
            self.message = "Can't place barriers in temples!"
        if reason == 'board':
            self.message = "This field does not exist!"
