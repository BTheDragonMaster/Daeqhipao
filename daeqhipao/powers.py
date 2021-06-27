from daeqhipao.illegal_moves import IllegalPower

class Power:
    def __init__(self, piece):
        self.target_nr = 0
        self.target_types = []
        self.piece = piece
        self.name = None

        self.selected_piece_1 = None
        self.selected_piece_2 = None
        self.selected_field_1 = None
        self.selected_field_2 = None
        self.selected_barrier_1 = None
        self.selected_barrier_2 = None

        self.targets_1 = []
        self.targets_2 = []

    def set_target_types(self, selection_types):
        self.target_nr = len(selection_types)
        self.target_types = selection_types

    def reset_targets(self):
        self.selected_piece_1 = None
        self.selected_piece_2 = None
        self.target_nr = len(self.target_types)
        self.targets_1 = []
        self.targets_2 = []

    def select_piece_1(self, piece, board):
        self.selected_piece_1 = piece
        self.target_nr -= 1

    def select_piece_2(self, piece, board):
        self.selected_piece_2 = piece
        self.target_nr -= 1

    def select_field_1(self, field, board):
        self.selected_field_1 = field
        self.target_nr -= 1

    def select_field_2(self, field, board):
        self.selected_field_2 = field
        self.target_nr -= 1

    def select_barrier_1(self, barrier, board):
        self.selected_barrier_1 = barrier
        self.target_nr -= 1

    def select_barrier_2(self, barrier, board):
        self.selected_barrier_2 = barrier
        self.target_nr -= 1

    def get_target_type(self):
        return self.target_types[-self.target_nr]

    def get_target_fields_1(self, *args):
        pass

    def get_target_fields_2(self, *args):
        pass

    def use_power(self, *args):
        pass

    def get_target_fields(self, pieces, barriers, board):

        targets = []

        if self.name == 'Union':
            if self.target_nr == 2:
                targets = self.get_target_fields_1(pieces.active_pieces, pieces.passive_pieces)
            elif self.target_nr == 1:
                targets = self.get_target_fields_2(pieces.active_pieces, pieces.passive_pieces)
        elif self.name == 'Impression':
            if self.target_nr == 1:
                targets = self.get_target_fields_1(pieces.pieces)

        return targets

    def activate_power(self, pieces, barriers, board):
        if self.name == 'Union':
            self.use_power()
        elif self.name == 'Impression':
            self.use_power(board)
        elif self.name == 'Communication':
            pass

        self.reset_targets()
        self.piece.sleep(pieces.active_pieces, pieces.passive_pieces)



class UnionPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Union'
        self.set_target_types(['piece', 'piece'])
        self.confirm_message = "Link the flip states of these pieces?"

    def use_power(self):
        self.piece.select_piece(self.selected_piece_1, self.piece.name)
        self.piece.select_piece(self.selected_piece_2, self.piece.name)

        if self.selected_piece_1.active != self.selected_piece_2.active:
            raise IllegalPower('union')

        self.selected_piece_1.activate_union(self.selected_piece_2)
        self.selected_piece_2.activate_union(self.selected_piece_1)

    def get_target_fields_1(self, active_pieces, passive_pieces):

        true_active_targets = []
        true_passive_targets = []

        targets = []

        for piece in active_pieces:
            if piece != self.piece and not piece.immune('Union'):
                true_active_targets.append(piece.location)

        for piece in passive_pieces:
            if piece != self.piece and not piece.immune('Union'):
                true_passive_targets.append(piece.location)

        if len(true_active_targets) >= 2:
            targets += true_active_targets

        if len(true_passive_targets) >= 2:
            targets += true_passive_targets

        return targets

    def get_target_fields_2(self, active_pieces, passive_pieces):

        targets = []

        if self.selected_piece_1.active:
            for piece in active_pieces:
                if piece != self.selected_piece_1 and piece != self.piece and not piece.immune("Union"):
                    targets.append(piece.location)

        else:
            for piece in passive_pieces:
                if piece != self.selected_piece_1 and piece != self.piece and not piece.immune("Union"):
                    targets.append(piece.location)

        return targets


class ImpressionPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Impression'
        self.set_target_types(['piece'])
        self.confirm_message = "Switch position with this piece?"

    def use_power(self, board, *args):
        self.piece.select_piece(self.selected_piece_1, self.piece.name)

        board.swap_objects(self.piece, self.selected_piece_1)



    def get_target_fields_1(self, pieces):

        targets = []

        for piece in pieces:
            if piece != self.piece and not piece.immune('Impression') and not piece.location.in_temple_area():
                targets.append(piece)

        return targets

class CommunicationPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Communication'
        self.set_target_types(['piece'])
        self.confirm_message = "Give this piece the option to move two extra times next turn (three times in total)_instead of using its power?"

class FamiliarityPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Familiarity'
        self.set_target_types(['piece', 'piece'])
        self.confirm_message = "Use this piece's power?"

class LifePower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Life'
        self.set_target_types(['piece'])
        self.confirm_message = "Bring this piece back to life?"

class PerceptionPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Perception'
        self.set_target_types(['piece'])
        self.confirm_message = "Make this piece immune?"

class MindPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Mind'
        self.set_target_types([])
        self.confirm_message = "Protect your temple from powers?"

class LegacyPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Legacy'
        self.set_target_types(['piece'])
        self.confirm_message = "Protect your temple from powers?"

class TimePower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Time'
        self.set_target_types(['player'])
        self.confirm_message = "Force this player to move two pieces next turn?"

class IllusionPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Illusion'
        self.set_target_types(['piece'])
        self.confirm_message = "Force this piece to move next turn?"

class IdeaPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Idea'
        self.set_target_types(['piece'])
        self.confirm_message = "Force this piece to use its power next turn?"

class MetamorphosisPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Metamorphosis'
        self.set_target_types(['piece', 'piece'])
        self.confirm_message = "Switch these two pieces and their ownership?"

class DeathPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Death'
        self.set_target_types(['piece'])
        self.confirm_message = "Kill this piece?"

class BlindnessPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Blindness'
        self.set_target_types(['piece'])
        self.confirm_message = "Prevent this piece from moving in the next two turns?"

class OblivionPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Oblivion'
        self.set_target_types(['piece'])
        self.confirm_message = "Prevent this piece resetting next Zaopeng?"

class LiberationPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Liberation'
        self.set_target_types(['piece'])
        self.confirm_message = "Prevent this piece from using its power in the next two turns?"

class EarthPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Earth'
        self.set_target_types(['choice', 'field', 'field'])
        self.confirm_message = "Place barriers here?"

class OceanPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Ocean'
        self.set_target_types(['field'])
        self.confirm_message = "Place ocean here?"

class SkyPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Sky'
        self.set_target_types(['piece'])
        self.confirm_message = "Jump here?"

class SunPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Sun'
        self.set_target_types(['field'])
        self.confirm_message = "Move here?"

class QuakePower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Quake'
        self.set_target_types(['barrier', 'field'])
        self.confirm_message = "Move barrier here?"

class WavePower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Wave'
        self.set_target_types(['piece', 'field'])
        self.confirm_message = "Move piece here?"

class WindPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Wind'
        self.set_target_types(['field'])
        self.confirm_message = "Move here?"

class ShadowPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Shadow'
        self.set_target_types(['barrier'])
        self.confirm_message = "Jump here?"

class MetalmakerPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Metalmaker'
        self.set_target_types(['field'])
        self.confirm_message = "Move and leave barrier?"

class BloodmakerPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Bloodmaker'
        self.set_target_types(['barrier', 'piece'])
        self.confirm_message = "Switch this barrier with this piece?"

class FogPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Fog'
        self.set_target_types(['piece', 'piece'])
        self.confirm_message = "Switch these pieces?"

class FlamePower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Flame'
        self.set_target_types([])
        self.confirm_message = "Activate flame?"

class VoidPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Void'
        self.set_target_types(['choice', 'barrier', 'barrier'])
        self.confirm_message = "Remove these barriers?"

class DroughtPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Drought'
        self.set_target_types(['field'])
        self.confirm_message = "Place drought here?"

class EndPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'End'
        self.set_target_types(['piece', 'field'])
        self.confirm_message = "Move this piece back to your temple area?"

class NightPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Night'
        self.set_target_types(['barrier'])
        self.confirm_message = "Consume this barrier?"