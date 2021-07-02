from daeqhipao.illegal_moves import IllegalPower

POTENCY = {'Perception', 'Mind', 'Blindness', 'Oblivion', 'Liberation', 'Flame', 'Communication', 'Idea', 'Illusion'}

FREQUENCY = {'Life', 'Perception', 'Union', 'Impression', 'Familiarity', 'Metamorphosis', 'Death', 'Blindness', 'Liberation',
             'Earth', 'Ocean', 'Sky', 'Sun', 'Quake', 'Wave', 'Wind', 'Shadow', 'Metalmaker', 'Bloodmaker',
             'Fog', 'Void', 'Drought', 'End', 'Night'}

class Power:
    def __init__(self, piece):
        self.target_nr = 0
        self.target_types = []
        self.piece = piece
        self.name = None
        self.start_with_choice = False

        self.choice = None
        self.selected_piece_1 = None
        self.selected_piece_2 = None
        self.selected_field_1 = None
        self.selected_field_2 = None
        self.selected_barrier_1 = None
        self.selected_barrier_2 = None

        self.targets_1 = []
        self.targets_2 = []
        self.highlight_types = []

        self.fixed_affected_area = False

    def set_target_types(self, selection_types):
        self.target_nr = len(selection_types)
        self.target_types = selection_types

    def highlight_all_targets(self, turn_manager, mouse):

        highlight_type = self.get_highlight_type()
        if highlight_type == 'highlight all targets':
            turn_manager.board.highlight_fields(self.piece.player, turn_manager.current_target_fields)
        elif highlight_type == 'hover':
            turn_manager.hover = True


    def highlight_hover(self, screen, board, target_fields, mouse):
        if self.name == 'Ocean' or self.name == 'Drought':
            hovered_field = None
            for field in target_fields:
                if field.rectangle.collidepoint(mouse):
                    hovered_field = field
                    break

            if hovered_field:

                for field in board.fields:
                    if not field.type == 'temple square':
                        if field.rectangle.collidepoint(mouse):
                            hovered = True
                        else:
                            adjacent_fields = field.get_adjacent(board, type='all')

                            if hovered_field in adjacent_fields:
                                hovered = True
                            else:
                                hovered = False

                        field.draw(screen, hovered, self.piece.player.colour_rgb)
                        if field.piece == self.piece:
                            field.draw(screen, True)

                        board.draw_frame()
                        field.draw_conditions(screen)
                        if field.piece:
                            board.draw_piece(field.piece)
                        elif field.barrier:
                            board.draw_barrier(field.barrier)
            else:
                for field in board.fields:
                    field.draw(screen, False, self.piece.player.colour_rgb)
                    if field.piece == self.piece:
                        field.draw(screen, True)

                    board.draw_frame()
                    field.draw_conditions(screen)
                    if field.piece:
                        board.draw_piece(field.piece)
                    elif field.barrier:
                        board.draw_barrier(field.barrier)


        else:
            for field in target_fields:

                if field.rectangle.collidepoint(mouse):
                    hovered = True
                else:
                    hovered = False



                field.draw(screen, hovered, self.piece.player.colour_rgb)
                if field.piece == self.piece:
                    field.draw(screen, True)

                if field == self.selected_field_1:
                    field.draw(screen, True, self.piece.player.colour_rgb_strong)

                board.draw_frame()
                field.draw_conditions(screen)
                if field.piece:
                    board.draw_piece(field.piece)
                elif field.barrier:
                    board.draw_barrier(field.barrier)


    def reset_targets(self):
        self.selected_piece_1 = None
        self.selected_piece_2 = None
        self.selected_field_1 = None
        self.selected_field_2 = None
        self.selected_barrier_1 = None
        self.selected_barrier_2 = None
        self.target_nr = len(self.target_types)
        self.targets_1 = []
        self.targets_2 = []
        self.choice = None

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

    def get_choices(self, barriers):

        choice_1 = None
        choice_2 = None

        if self.name == 'Earth':
            if len(barriers.used_barriers) <= 1:
                choice_1 = 'Place 1 barrier'
                choice_2 = 'Place 2 barriers'
            elif len(barriers.used_barriers) == 2:
                choice_1 = 'Place 1 barrier'
                choice_2 = None
            else:
                raise IllegalPower("Earth can't use its power!")

        elif self.name == 'Void':
            if len(barriers.used_barriers) >= 2:
                choice_1 = 'Remove 1 barrier'
                choice_2 = 'Remove 2 barriers'
            elif len(barriers.used_barriers) == 1:
                choice_1 = 'Remove 1 barrier'
                choice_2 = None
            else:
                raise IllegalPower("Void can't use its power!")

        return choice_1, choice_2

    def get_target_type(self):
        return self.target_types[-self.target_nr]

    def get_highlight_type(self):
        return self.highlight_types[-self.target_nr]

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
        elif self.name == 'Earth':
            if self.target_nr == 2:
                targets = self.get_target_fields_1(board)
            elif self.target_nr == 1:
                targets = self.get_target_fields_2(board)
        elif self.name == 'Void':
            if self.target_nr == 2:
                targets = self.get_target_fields_1(board)
            elif self.target_nr == 1:
                targets = self.get_target_fields_2(board)
        elif self.name == 'Ocean':
            targets = self.get_target_fields_1(board)
        elif self.name == 'Drought':
            targets = self.get_target_fields_1(board)
        elif self.name == 'Life':
            targets = self.get_target_fields_1(pieces)
        elif self.name == 'Death':
            targets = self.get_target_fields_1(pieces)


        return targets

    def activate_power(self, pieces, barriers, board):
        if self.name == 'Union':
            self.use_power()
        elif self.name == 'Impression':
            self.use_power(board)
        elif self.name == 'Earth':
            self.use_power(barriers, board)
        elif self.name == 'Void':
            self.use_power(barriers, board)
        elif self.name == 'Communication':
            pass
        elif self.name == 'Ocean':
            self.use_power(board)
        elif self.name == 'Drought':
            self.use_power(board)
        elif self.name == "Life":
            self.use_power(pieces)
        elif self.name == "Death":
            self.use_power(pieces)

        self.reset_targets()
        self.piece.sleep(pieces)


class UnionPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Union'
        self.set_target_types(['piece', 'piece'])
        self.confirm_message = "Link the flip states of these pieces?"
        self.highlight_types = ["highlight all targets", "highlight all targets"]

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
        self.highlight_types = ["highlight all targets"]

    def use_power(self, board, *args):
        self.piece.select_piece(self.selected_piece_1, self.piece.name)

        board.swap_objects(self.piece, self.selected_piece_1)


    def get_target_fields_1(self, pieces):

        targets = []

        for piece in pieces:
            if piece != self.piece and not piece.immune('Impression') and not piece.location.in_temple_area():
                targets.append(piece.location)

        return targets

class CommunicationPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Communication'
        self.set_target_types(['piece'])
        self.confirm_message = "Give this piece the option to move two extra times next turn (three times in total)_instead of using its power?"
        self.highlight_types = ["highlight all targets"]

class FamiliarityPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Familiarity'
        self.set_target_types(['piece', 'piece'])
        self.confirm_message = "Borrow this piece's power?"
        self.highlight_types = ["highlight all targets", "highlight all targets"]

class LifePower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Life'
        self.set_target_types(['piece'])
        self.confirm_message = "Bring this piece back to life?"
        self.highlight_types = ["highlight all targets"]

    def get_target_fields_1(self, pieces):

        targets = []

        for piece in pieces.pieces:
            if piece != self.piece and not piece.immune('Life') and not piece.active:
                targets.append(piece.location)

        return targets

    def use_power(self, pieces):
        self.selected_piece_1.wake(pieces)


class PerceptionPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Perception'
        self.set_target_types(['piece'])
        self.confirm_message = "Make this piece immune?"
        self.highlight_types = ["highlight all targets"]

class MindPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Mind'
        self.set_target_types([])
        self.confirm_message = "Protect your temple from powers?"
        self.highlight_types = []
        self.fixed_affected_area = True

class LegacyPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Legacy'
        self.set_target_types(['piece'])
        self.confirm_message = "Allow this spiritual piece to increase the frequency or duration of its power next turn, or allow this Spiritual God piece to use two powers next turn?"
        self.highlight_types = ["highlight all targets"]

class TimePower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Time'
        self.set_target_types(['piece'])
        self.confirm_message = "Allow this physical piece to increase the frequency or duration of its power next turn, or allow this Physical God piece to use two powers next turn?"
        self.highlight_types = ["highlight all targets"]

class IllusionPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Illusion'
        self.set_target_types(['piece'])
        self.confirm_message = "Force this piece to move next turn?"
        self.highlight_types = ["highlight all targets"]

class IdeaPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Idea'
        self.set_target_types(['piece'])
        self.confirm_message = "Force this piece to use its power next turn?"
        self.highlight_types = ["highlight all targets"]

class MetamorphosisPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Metamorphosis'
        self.set_target_types(['piece', 'piece'])
        self.confirm_message = "Switch these two pieces and their ownership?"
        self.highlight_types = ["highlight all targets", "highlight all targets"]

class DeathPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Death'
        self.set_target_types(['piece'])
        self.confirm_message = "Kill this piece?"
        self.highlight_types = ["highlight all targets"]

    def get_target_fields_1(self, pieces):

        targets = []

        for piece in pieces.pieces:
            if piece != self.piece and not piece.immune('Death') and piece.active:
                targets.append(piece.location)

        return targets

    def use_power(self, pieces):
        self.selected_piece_1.sleep(pieces)

class BlindnessPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Blindness'
        self.set_target_types(['piece'])
        self.confirm_message = "Prevent this piece from moving in the next two turns?"
        self.highlight_types = ["highlight all targets"]

class OblivionPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Oblivion'
        self.set_target_types(['piece'])
        self.confirm_message = "Prevent this piece resetting next Zaopeng?"
        self.highlight_types = ["highlight all targets"]

class LiberationPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Liberation'
        self.set_target_types(['piece'])
        self.confirm_message = "Prevent this piece from using its power in the next two turns?"
        self.highlight_types = ["highlight all targets"]

class EarthPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Earth'
        self.set_target_types(['field', 'field'])
        self.confirm_message = "Place barriers here?"
        self.start_with_choice = True
        self.highlight_types = ["hover", "hover"]

    def get_target_fields_1(self, board):
        target_fields = []

        for field in board.fields:
            if not field.occupied and not field.type == 'temple square':
                target_fields.append(field)

        return target_fields

    def get_target_fields_2(self, board):
        target_fields = []

        for field in board.fields:
            if not field == self.selected_field_1 and not field.occupied and not field.type == 'temple square':
                target_fields.append(field)

        return target_fields

    def use_power(self, barriers, board):
        if self.selected_field_1:
            barrier = barriers.unused_barriers[0]
            barrier.place_on_board(self.selected_field_1, board, barriers)
        if self.selected_field_2:
            barrier = barriers.unused_barriers[0]
            barrier.place_on_board(self.selected_field_2, board, barriers)


class OceanPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Ocean'
        self.set_target_types(['field'])
        self.confirm_message = "Place ocean here?"
        self.highlight_types = ["hover"]

    def get_target_fields_1(self, board):
        target_fields = []

        for field in board.fields:
            if not field.type == 'temple square' and not field.in_temple_area():
                target_fields.append(field)

        return target_fields

    def use_power(self, board):
        adjacent_squares = self.selected_field_1.get_adjacent(board)
        self.selected_field_1.activate_ocean(self.piece)
        for adjacent_square in adjacent_squares:
            if adjacent_square.type != 'temple square':
                adjacent_square.activate_ocean(self.piece)


class SkyPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Sky'
        self.set_target_types(['field'])
        self.confirm_message = "Jump here?"
        self.highlight_types = ["highlight all targets"]


class SunPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Sun'
        self.set_target_types(['field'])
        self.confirm_message = "Move here?"
        self.highlight_types = ["highlight all targets"]


class QuakePower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Quake'
        self.set_target_types(['barrier', 'field'])
        self.confirm_message = "Move barrier here?"
        self.highlight_types = ["highlight all targets", "hover"]


class WavePower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Wave'
        self.set_target_types(['piece', 'field'])
        self.confirm_message = "Move piece here?"
        self.highlight_types = ["highlight all targets", "highlight all targets"]


class WindPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Wind'
        self.set_target_types(['field'])
        self.confirm_message = "Move here?"
        self.highlight_types = ["highlight all targets"]


class ShadowPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Shadow'
        self.set_target_types(['field'])
        self.confirm_message = "Jump here?"
        self.highlight_types = ["highlight all targets"]


class MetalmakerPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Metalmaker'
        self.set_target_types(['field'])
        self.confirm_message = "Move and leave barrier?"
        self.highlight_types = ["highlight all targets"]


class BloodmakerPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Bloodmaker'
        self.set_target_types(['barrier', 'piece'])
        self.confirm_message = "Switch this barrier with this piece?"
        self.highlight_types = ["highlight all targets", "highlight all targets"]


class FogPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Fog'
        self.set_target_types(['piece', 'piece'])
        self.confirm_message = "Switch these pieces?"
        self.highlight_types = ["highlight all targets", "highlight all targets"]


class FlamePower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Flame'
        self.set_target_types([])
        self.confirm_message = "Activate flame?"
        self.highlight_types = []
        self.fixed_affected_area = True


class VoidPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Void'
        self.set_target_types(['barrier', 'barrier'])
        self.confirm_message = "Remove these barriers?"
        self.highlight_types = ["highlight all targets", "highlight all targets"]
        self.start_with_choice = True

    def get_target_fields_1(self, board):
        target_fields = []

        for field in board.fields:
            if field.barrier:
                target_fields.append(field)

        return target_fields

    def get_target_fields_2(self, board):
        target_fields = []

        for field in board.fields:
            if field.barrier and not field == self.selected_field_1:
                target_fields.append(field)

        return target_fields

    def use_power(self, barriers, board):
        if self.selected_barrier_1:
            self.selected_barrier_1.remove_from_board(board, barriers)
        if self.selected_barrier_2:
            self.selected_barrier_2.remove_from_board(board, barriers)


class DroughtPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Drought'
        self.set_target_types(['field'])
        self.confirm_message = "Place drought here?"
        self.highlight_types = ["hover"]

    def get_target_fields_1(self, board):
        target_fields = []

        for field in board.fields:
            if not field.type == 'temple square' and not field.in_temple_area():
                target_fields.append(field)

        return target_fields

    def use_power(self, board):
        adjacent_squares = self.selected_field_1.get_adjacent(board)
        self.selected_field_1.activate_drought(self.piece)
        for adjacent_square in adjacent_squares:
            if adjacent_square.type != 'temple square':
                adjacent_square.activate_drought(self.piece)


class EndPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'End'
        self.set_target_types(['piece', 'field'])
        self.confirm_message = "Move this piece back to your temple area?"
        self.highlight_types = ["highlight all targets", "highlight all targets"]


class NightPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Night'
        self.set_target_types(['barrier'])
        self.confirm_message = "Consume this barrier?"
        self.highlight_types = ["highlight all targets"]