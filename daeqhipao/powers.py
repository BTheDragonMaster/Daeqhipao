from daeqhipao.illegal_moves import IllegalPower

POTENCY = {'Perception', 'Mind', 'Blindness', 'Oblivion', 'Liberation', 'Flame', 'Communication', 'Idea', 'Illusion', 'Director', 'Wiper', 'Connector', 'Gifter', 'Alchemist'}

FREQUENCY = {'Life', 'Perception', 'Union', 'Impression', 'Familiarity', 'Metamorphosis', 'Death', 'Blindness', 'Liberation',
             'Earth', 'Ocean', 'Sky', 'Sun', 'Quake', 'Wave', 'Wind', 'Shadow', 'Metalmaker', 'Bloodmaker',
             'Fog', 'Void', 'Drought', 'End', 'Night', 'Gifter', 'Connector', 'Director', 'Wiper', 'Builder', 'Mover', 'Alchemist', 'Consumer'}

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

        self.potency_or_frequency = None

        self.targets_1 = []
        self.targets_2 = []
        self.highlight_types = []

        self.fixed_affected_area = False

    def check_power_usable(self, pieces, barriers, board, players):
        if not self.piece.active:
            return False
        if self.fixed_affected_area:
            return True
        targets = self.get_target_fields(pieces, barriers, board, players)

        if not targets:
            return False
        return True


    def set_target_types(self, selection_types):
        self.target_nr = len(selection_types)
        self.target_types = selection_types

    def highlight_all_targets(self, turn_manager):

        highlight_type = self.get_highlight_type()
        if highlight_type == 'highlight all targets':
            turn_manager.board.highlight_fields(self.piece.player, turn_manager.current_target_fields)
        elif highlight_type == 'hover':
            turn_manager.hover = True

    def highlight_selected_fields(self, screen, board):
        fields_to_highlight = []
        if self.selected_field_1:
            fields_to_highlight.append(self.selected_field_1)
        if self.selected_field_2:
            fields_to_highlight.append(self.selected_field_2)
        if self.selected_piece_1:
            fields_to_highlight.append(self.selected_piece_1.location)
        if self.selected_piece_2:
            fields_to_highlight.append(self.selected_piece_2.location)
        if self.selected_barrier_1:
            fields_to_highlight.append(self.selected_barrier_1.location)
        if self.selected_barrier_2:
            fields_to_highlight.append(self.selected_barrier_2.location)

        for field in fields_to_highlight:
            field.highlight_strong(screen, self.piece.player, board)

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

    def select_piece_1(self, piece):
        self.selected_piece_1 = piece
        self.target_nr -= 1

    def select_piece_2(self, piece):
        self.selected_piece_2 = piece
        self.target_nr -= 1

    def select_field_1(self, field):
        self.selected_field_1 = field
        self.target_nr -= 1

    def select_field_2(self, field):
        self.selected_field_2 = field
        self.target_nr -= 1

    def select_barrier_1(self, barrier):
        self.selected_barrier_1 = barrier
        self.target_nr -= 1

    def select_barrier_2(self, barrier):
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

        if self.name == 'Time' or self.name == 'Legacy':
            choice_1 = 'Increase potency'
            choice_2 = 'Increase frequency'

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

    def get_target_fields(self, pieces, barriers, board, players):

        targets = []

        if self.name == 'Union':
            if self.target_nr == 2:
                targets = self.get_target_fields_1(pieces)
            elif self.target_nr == 1:
                targets = self.get_target_fields_2(pieces)
        elif self.name == 'Impression':
            if self.target_nr == 1:
                targets = self.get_target_fields_1(pieces)
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
        elif self.name == 'Sun':
            targets = self.get_target_fields_1(board)
        elif self.name == 'Wind':
            targets = self.get_target_fields_1(board)
        elif self.name == 'Sky':
            targets = self.get_target_fields_1(board)
        elif self.name == 'Shadow':
            targets = self.get_target_fields_1(board)
        elif self.name == 'Idea':
            targets = self.get_target_fields_1(players, pieces)
        elif self.name == 'Illusion':
            targets = self.get_target_fields_1(players, pieces)
        elif self.name == 'Quake':
            if self.target_nr == 2:
                targets = self.get_target_fields_1(board)
            elif self.target_nr == 1:
                targets = self.get_target_fields_2(board)
        elif self.name == 'Wave':
            if self.target_nr == 2:
                targets = self.get_target_fields_1(board, pieces)
            elif self.target_nr == 1:
                targets = self.get_target_fields_2(board)
        elif self.name == 'Fog':
            if self.target_nr == 2:
                targets = self.get_target_fields_1(board, pieces)
            elif self.target_nr == 1:
                targets = self.get_target_fields_2(board)
        elif self.name == 'Bloodmaker':
            if self.target_nr == 2:
                targets = self.get_target_fields_1(board)
            elif self.target_nr == 1:
                targets = self.get_target_fields_2(board)
        elif self.name == 'Metalmaker':
            targets = self.get_target_fields_1(board, barriers)
        elif self.name == 'Night':
            targets = self.get_target_fields_1(board)
        elif self.name == 'End':
            if self.target_nr == 2:
                targets = self.get_target_fields_1(pieces, board)
            elif self.target_nr == 1:
                targets = self.get_target_fields_2(board)
        elif self.name == 'Time':
            targets = self.get_target_fields_1(pieces)
        elif self.name == 'Legacy':
            targets = self.get_target_fields_1(pieces)
        elif self.name == 'Metamorphosis':
            if self.target_nr == 2:
                targets = self.get_target_fields_1(pieces)
            elif self.target_nr == 1:
                targets = self.get_target_fields_2(pieces)

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
        elif self.name == 'Sun':
            self.use_power(board)
        elif self.name == 'Wind':
            self.use_power(board)
        elif self.name == 'Sky':
            self.use_power(board)
        elif self.name == 'Shadow':
            self.use_power(board)
        elif self.name == 'Idea':
            self.use_power()
        elif self.name == 'Illusion':
            self.use_power()
        elif self.name == 'Quake':
            self.use_power(board)
        elif self.name == 'Wave':
            self.use_power(board)
        elif self.name == 'Fog':
            self.use_power(board)
        elif self.name == 'Bloodmaker':
            self.use_power(board)
        elif self.name == 'Metalmaker':
            self.use_power(board, barriers)
        elif self.name == 'Flame':
            self.use_power(board)
        elif self.name == 'Night':
            self.use_power(board, barriers)
        elif self.name == 'End':
            self.use_power(board)
        elif self.name == 'Mind':
            self.use_power(board)
        elif self.name == 'Legacy':
            self.use_power()
        elif self.name == 'Time':
            self.use_power()
        elif self.name == 'Metamorphosis':
            self.use_power(board, pieces)

        self.reset_targets()
        self.piece.deactivate_idea()
        if not self.piece.frequency:
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

    def get_target_fields_1(self, pieces):

        true_active_targets = []
        true_passive_targets = []

        targets = []

        for piece in pieces.active_pieces:
            if piece != self.piece and not piece.immune('Union'):
                true_active_targets.append(piece.location)

        for piece in pieces.passive_pieces:
            if piece != self.piece and not piece.immune('Union'):
                true_passive_targets.append(piece.location)

        if len(true_active_targets) >= 2:
            targets += true_active_targets

        if len(true_passive_targets) >= 2:
            targets += true_passive_targets

        return targets

    def get_target_fields_2(self, pieces):

        targets = []

        if self.selected_piece_1.active:
            for piece in pieces.active_pieces:
                if piece != self.selected_piece_1 and piece != self.piece and not piece.immune("Union"):
                    targets.append(piece.location)

        else:
            for piece in pieces.passive_pieces:
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

        for piece in pieces.pieces:
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

    def use_power(self):
        self.selected_piece_1.activate_communication(self.piece, self.piece.potency)

    def get_target_fields_1(self, pieces):
        targets = []
        for piece in pieces.pieces:
            if not piece.immune('Communication'):
                targets.append(piece)


class FamiliarityPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Familiarity'
        self.set_target_types(['piece'])
        self.confirm_message = "Borrow this piece's power?"
        self.highlight_types = ["highlight all targets"]


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

    def use_power(self):
        self.selected_piece_1.activate_perception(self.piece)

    def get_target_fields_1(self, pieces):
        target_fields = []

        for piece in pieces.pieces:
            if not piece.immune("Perception"):
                target_fields.append(piece.location)
        return target_fields


class MindPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Mind'
        self.set_target_types([])
        self.confirm_message = "Protect your temple from powers?"
        self.highlight_types = []
        self.fixed_affected_area = True

    def use_power(self, board):
        board.temple_squares[self.piece.player].mind = True

    def get_target_fields_1(self, board):
        return [board.temple_squares[self.piece.player]]


class LegacyPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Legacy'
        self.set_target_types(['piece'])
        self.confirm_message = "Allow this spiritual piece to increase the frequency or duration of its power next turn, or allow this Spiritual God piece to use two powers next turn?"
        self.highlight_types = ["highlight all targets"]
        self.start_with_choice = True

    def use_power(self):
        if self.potency_or_frequency == 'potency':
            self.selected_piece_1.set_potency(self.piece)

        elif self.potency_or_frequency == 'frequency':
            self.selected_piece_1.set_frequency(self.piece)

    def get_target_fields_1(self, pieces):
        target_fields = []
        for piece in pieces.spiritual_pieces:
            if not piece.immune('Legacy'):
                if self.potency_or_frequency == 'potency' and piece.name in POTENCY:
                    target_fields.append(piece.location)
                elif self.potency_or_frequency == 'frequency' and piece.name in FREQUENCY:
                    target_fields.append(piece.location)
                elif not self.potency_or_frequency and (piece.name in POTENCY or piece.name in FREQUENCY):
                    target_fields.append(piece.location)

        return target_fields


class TimePower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Time'
        self.set_target_types(['piece'])
        self.confirm_message = "Allow this physical piece to increase the frequency or duration of its power next turn, or allow this Physical God piece to use two powers next turn?"
        self.highlight_types = ["highlight all targets"]
        self.start_with_choice = True

    def use_power(self):
        if self.potency_or_frequency == 'potency':
            self.selected_piece_1.set_potency(self.piece)

        elif self.potency_or_frequency == 'frequency':
            self.selected_piece_1.set_frequency(self.piece)


    def get_target_fields_1(self, pieces):
        target_fields = []
        for piece in pieces.physical_pieces:
            if not piece.immune('Time'):
                if self.potency_or_frequency == 'potency' and piece.name in POTENCY:
                    target_fields.append(piece.location)
                elif self.potency_or_frequency == 'frequency' and piece.name in FREQUENCY:
                    target_fields.append(piece.location)
                elif not self.potency_or_frequency and (piece.name in POTENCY or piece.name in FREQUENCY):
                    target_fields.append(piece.location)

        return target_fields


class IllusionPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Illusion'
        self.set_target_types(['piece'])
        self.confirm_message = "Force this piece to move next turn?"
        self.highlight_types = ["highlight all targets"]

    def use_power(self):
        self.selected_piece_1.activate_illusion()

    def get_target_fields_1(self, players, pieces):
        idea_players = []
        legal_players = []

        for player in players:
            if player != self.piece.player and not player.illusion:
                if player.idea:
                    idea_players.append(player)
                else:
                    legal_players.append(player)

        target_fields = []

        for piece in pieces.pieces:
            if piece.active and not piece.immune('Illusion'):
                if piece.player in legal_players:
                    target_fields.append(piece.location)
                elif piece.player in idea_players:
                    if piece.idea:
                        target_fields.append(piece.location)

        return target_fields

class IdeaPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Idea'
        self.set_target_types(['piece'])
        self.confirm_message = "Force this piece to use its power next turn?"
        self.highlight_types = ["highlight all targets"]

    def use_power(self):
        self.selected_piece_1.activate_idea()

    def get_target_fields_1(self, players, pieces):
        illusion_players = []
        legal_players = []

        for player in players:
            if player != self.piece.player and not player.idea:
                if player.illusion:
                    illusion_players.append(player)
                else:
                    legal_players.append(player)

        target_fields = []

        for piece in pieces.pieces:
            if piece.active and not piece.immune('Idea'):
                if piece.player in legal_players:
                    target_fields.append(piece.location)
                elif piece.player in illusion_players:
                    if piece.illusion:
                        target_fields.append(piece.location)

        return target_fields

class MetamorphosisPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Metamorphosis'
        self.set_target_types(['piece', 'piece'])
        self.confirm_message = "Switch these two pieces and their ownership?"
        self.highlight_types = ["highlight all targets", "highlight all targets"]

    def use_power(self, board, pieces):

        original_player_1 = self.selected_piece_1.player
        original_player_2 = self.selected_piece_2.player

        if original_player_1 != original_player_2:
            self.selected_piece_1.player = original_player_2
            self.selected_piece_2.player = original_player_1
        board.swap_objects(self.selected_piece_1, self.selected_piece_2)

    def get_target_fields_1(self, pieces):

        targets = []

        for name, god_group in pieces.god_groups.items():
            true_targets = []
            if len(god_group) > 1:
                for piece in god_group:
                    if piece.active and not piece.immune('Metamorphosis'):
                        true_targets.append(piece.location)

            if len(true_targets) > 1:
                targets += true_targets

        return targets

    def get_target_fields_2(self, pieces):
        targets = []
        for piece in pieces.god_groups[self.selected_piece_1.god_group]:
            if piece.active and not piece == self.selected_piece_1 and not piece.immune('Metamorphosis'):
                targets.append(piece.location)

        return targets


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

    def use_power(self, board):
        self.piece.move(self.selected_field_1, board)

    def get_target_fields_1(self, board):
        adjacent_fields = self.piece.location.get_adjacent(board, type='all')
        adjacent_fields_with_pieces = []
        for adjacent_field in adjacent_fields:
            if adjacent_field.piece and not adjacent_field.piece.immune('Sky'):
                adjacent_fields_with_pieces.append(adjacent_field)

        jump_locations = []

        for field in adjacent_fields_with_pieces:
            diff_x = field.x - self.piece.location.x
            diff_y = field.y - self.piece.location.y
            jump_location = board.get_field(field.x + diff_x, field.y + diff_y)
            if jump_location and jump_location.check_legal_movement(self.piece, using_power=True):
                jump_locations.append(jump_location)

        return jump_locations


class SunPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Sun'
        self.set_target_types(['field'])
        self.confirm_message = "Move here?"
        self.highlight_types = ["highlight all targets"]

    def use_power(self, board):
        self.piece.move(self.selected_field_1, board)

    def get_target_fields_1(self, board):

        target_1 = board.get_field(self.piece.location.x + 2, self.piece.location.y)
        target_2 = board.get_field(self.piece.location.x - 2, self.piece.location.y)
        target_3 = board.get_field(self.piece.location.x, self.piece.location.y + 2)
        target_4 = board.get_field(self.piece.location.x, self.piece.location.y - 2)

        pass_1 = board.get_field(self.piece.location.x + 1, self.piece.location.y)
        pass_2 = board.get_field(self.piece.location.x - 1, self.piece.location.y)
        pass_3 = board.get_field(self.piece.location.x, self.piece.location.y + 1)
        pass_4 = board.get_field(self.piece.location.x, self.piece.location.y - 1)

        target_fields = []
        if self.check_target(target_1, pass_1):
            target_fields.append(target_1)
        if self.check_target(target_2, pass_2):
            target_fields.append(target_2)
        if self.check_target(target_3, pass_3):
            target_fields.append(target_3)
        if self.check_target(target_4, pass_4):
            target_fields.append(target_4)

        return target_fields

    def check_target(self, target_field, pass_through_field):
        if not target_field:
            return False
        if target_field.type == 'no field':
            return False
        if not pass_through_field:
            return False
        if pass_through_field.type == 'no field':
            return False
        if target_field.check_legal_movement(self.piece, using_power=True) and pass_through_field.check_legal_movement(self.piece, using_power=True):
            return True
        else:
            return False


class QuakePower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Quake'
        self.set_target_types(['barrier', 'field'])
        self.confirm_message = "Move barrier here?"
        self.highlight_types = ["highlight all targets", "hover"]

    def use_power(self, board):
        self.selected_barrier_1.move(self.selected_field_1, board)

    def get_target_fields_1(self, board):
        target_fields = []

        for field in board.fields:
            if field.barrier:
                target_fields.append(field)

        return target_fields

    def get_target_fields_2(self, board):
        target_fields = []

        for field in board.fields:
            if not field.occupied and not field.type == 'temple square':
                target_fields.append(field)

        return target_fields


class WavePower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Wave'
        self.set_target_types(['piece', 'field'])
        self.confirm_message = "Move piece here?"
        self.highlight_types = ["highlight all targets", "highlight all targets"]

    def use_power(self, board):
        self.selected_piece_1.move(self.selected_field_1, board)

    def get_target_fields_1(self, board, pieces):
        target_fields = []
        for piece in pieces.pieces:
            if not piece.immune('Wave'):
                adjacent_fields = piece.location.get_adjacent(board, type='all')
                possible_movement = False
                for adjacent_field in adjacent_fields:
                    if adjacent_field.check_legal_movement(piece, using_power=True):
                        possible_movement = True
                        break
                if possible_movement:
                    target_fields.append(piece.location)

        return target_fields

    def get_target_fields_2(self, board):
        target_fields = []

        adjacent_fields = self.selected_piece_1.location.get_adjacent(board, type='all')

        for adjacent_field in adjacent_fields:
            if adjacent_field.check_legal_movement(self.selected_piece_1, using_power=True):
                target_fields.append(adjacent_field)

        return target_fields


class WindPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Wind'
        self.set_target_types(['field'])
        self.confirm_message = "Move here?"
        self.highlight_types = ["highlight all targets"]

    def use_power(self, board):
        self.piece.move(self.selected_field_1, board)

    def get_target_fields_1(self, board):

        target_1 = board.get_field(self.piece.location.x + 2, self.piece.location.y + 2)
        target_2 = board.get_field(self.piece.location.x - 2, self.piece.location.y + 2)
        target_3 = board.get_field(self.piece.location.x + 2, self.piece.location.y - 2)
        target_4 = board.get_field(self.piece.location.x - 2, self.piece.location.y - 2)

        pass_1 = board.get_field(self.piece.location.x + 1, self.piece.location.y + 1)
        pass_2 = board.get_field(self.piece.location.x - 1, self.piece.location.y + 1)
        pass_3 = board.get_field(self.piece.location.x + 1, self.piece.location.y - 1)
        pass_4 = board.get_field(self.piece.location.x - 1, self.piece.location.y - 1)

        target_fields = []
        if self.check_target(target_1, pass_1):
            target_fields.append(target_1)
        if self.check_target(target_2, pass_2):
            target_fields.append(target_2)
        if self.check_target(target_3, pass_3):
            target_fields.append(target_3)
        if self.check_target(target_4, pass_4):
            target_fields.append(target_4)

        return target_fields

    def check_target(self, target_field, pass_through_field):
        if not target_field:
            return False
        if target_field.type == 'no field':
            return False
        if not pass_through_field:
            return False
        if pass_through_field.type == 'no field':
            return False
        if target_field.check_legal_movement(self.piece, using_power=True) and pass_through_field.check_legal_movement(self.piece, using_power=True):
            return True
        else:
            return False


class ShadowPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Shadow'
        self.set_target_types(['field'])
        self.confirm_message = "Jump here?"
        self.highlight_types = ["highlight all targets"]

    def use_power(self, board):
        self.piece.move(self.selected_field_1, board)

    def get_target_fields_1(self, board):
        adjacent_fields = self.piece.location.get_adjacent(board, type='all')
        adjacent_fields_with_barriers = []
        for adjacent_field in adjacent_fields:
            if adjacent_field.barrier :
                adjacent_fields_with_barriers.append(adjacent_field)

        jump_locations = []

        for field in adjacent_fields_with_barriers:
            diff_x = field.x - self.piece.location.x
            diff_y = field.y - self.piece.location.y
            jump_location = board.get_field(field.x + diff_x, field.y + diff_y)
            if jump_location and jump_location.check_legal_movement(self.piece, using_power=True):
                jump_locations.append(jump_location)

        return jump_locations


class MetalmakerPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Metalmaker'
        self.set_target_types(['field'])
        self.confirm_message = "Move and leave barrier?"
        self.highlight_types = ["highlight all targets"]

    def use_power(self, board, barriers):
        field_of_origin = board.get_field(self.piece.location.x, self.piece.location.y)
        self.piece.move(self.selected_field_1, board)
        barrier = barriers.unused_barriers[0]
        barrier.place_on_board(field_of_origin, board, barriers)

    def get_target_fields_1(self, board, barriers):
        targets = []

        if barriers.unused_barriers:

            adjacent_fields = self.piece.location.get_adjacent(board, type='all')
            for field in adjacent_fields:
                if field.check_legal_movement(self.piece, using_power=True):
                    targets.append(field)

        return targets



class BloodmakerPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Bloodmaker'
        self.set_target_types(['barrier', 'piece'])
        self.confirm_message = "Switch this barrier with this piece?"
        self.highlight_types = ["highlight all targets", "highlight all targets"]

    def use_power(self, board):
        board.swap_objects(self.selected_barrier_1, self.selected_piece_1)

    def get_target_fields_1(self, board):

        targets = []

        for field in board.fields:
            if field.barrier:
                adjacent_fields = field.barrier.location.get_adjacent(board, type='all')
                potential_target = False
                for adjacent_field in adjacent_fields:
                    if adjacent_field.piece and self.check_swap_legal(field.barrier, adjacent_field.piece):
                        potential_target = True
                        break
                if potential_target:
                    targets.append(field.barrier.location)

        return targets

    def get_target_fields_2(self, board):
        targets = []
        adjacent_fields = self.selected_barrier_1.location.get_adjacent(board, type='all')
        for adjacent_field in adjacent_fields:
            if adjacent_field.piece and self.check_swap_legal(self.selected_barrier_1, adjacent_field.piece):
                targets.append(adjacent_field)

        return targets

    def check_swap_legal(self, barrier, piece):
        if piece.immune('Bloodmaker'):
            return False
        if not barrier.location.permitted_area_condition(piece):
            return False

        return True



class FogPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Fog'
        self.set_target_types(['piece', 'piece'])
        self.confirm_message = "Switch these pieces?"
        self.highlight_types = ["highlight all targets", "highlight all targets"]

    def use_power(self, board):
        board.swap_objects(self.selected_piece_1, self.selected_piece_2)

    def get_target_fields_1(self, board, pieces):

        targets = []

        for piece in pieces.pieces:
            if not piece.immune('Fog'):
                adjacent_fields = piece.location.get_adjacent(board, type='all')
                potential_target = False
                for adjacent_field in adjacent_fields:
                    if adjacent_field.piece and self.check_swap_legal(piece, adjacent_field.piece):
                        potential_target = True
                        break
                if potential_target:
                    targets.append(piece.location)

        return targets

    def get_target_fields_2(self, board):
        targets = []
        adjacent_fields = self.selected_piece_1.location.get_adjacent(board, type='all')
        for adjacent_field in adjacent_fields:
            if adjacent_field.piece and self.check_swap_legal(self.selected_piece_1, adjacent_field.piece):
                targets.append(adjacent_field)

        return targets

    def check_swap_legal(self, piece_1, piece_2):
        if piece_1.immune('Fog'):
            return False
        if piece_2.immune('Fog'):
            return False
        if not piece_1.location.permitted_area_condition(piece_2):
            return False
        if not piece_2.location.permitted_area_condition(piece_1):
            return False

        return True


class FlamePower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Flame'
        self.set_target_types([])
        self.confirm_message = "Activate flame?"
        self.highlight_types = []
        self.fixed_affected_area = True

    def use_power(self, board):
        for field in self.get_affected_fields(board):
            field.activate_flame(self.piece)

    def get_target_fields_1(self, board):
        target_fields = self.get_affected_fields(board)
        return target_fields

    def get_affected_fields(self, board):
        affected_fields = [self.piece.location]
        adjacent_fields = self.piece.location.get_adjacent(board, type='all')
        for field in adjacent_fields:
            if not (field.type == 'temple square' and field.owner):
                affected_fields.append(field)

        field_1 = board.get_field(self.piece.location.x, self.piece.location.y + 2)
        if field_1 and not field_1.type == 'temple square':
            affected_fields.append(field_1)

        field_2 = board.get_field(self.piece.location.x, self.piece.location.y - 2)
        if field_2 and not field_2.type == 'temple square':
            affected_fields.append(field_2)

        field_3 = board.get_field(self.piece.location.x + 2, self.piece.location.y)
        if field_3 and not field_3.type == 'temple square':
            affected_fields.append(field_3)

        field_4 = board.get_field(self.piece.location.x - 2, self.piece.location.y)
        if field_4 and not field_4.type == 'temple square':
            affected_fields.append(field_4)

        return affected_fields


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
            if field.barrier and not field.barrier == self.selected_barrier_1:
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
        self.confirm_message = "Move this piece back to their temple area?"
        self.highlight_types = ["highlight all targets", "highlight all targets"]

    def use_power(self, board):
        self.selected_piece_1.move(self.selected_field_1, board)

    def get_target_fields_1(self, pieces, board):
        target_fields = []
        for piece in pieces.pieces:
            if not piece.immune('End'):
                if not piece.location.in_temple_area():
                    temple_area = board.get_temple_area(piece.player)
                    for field in temple_area:
                        if field.check_legal_movement(piece, using_power=True):
                            target_fields.append(piece.location)
                            break

        return target_fields

    def get_target_fields_2(self, board):
        target_fields = []
        temple_area = board.get_temple_area(self.selected_piece_1.player)
        for field in temple_area:
            if field.check_legal_movement(self.selected_piece_1, using_power=True):
                target_fields.append(field)

        return target_fields


class NightPower(Power):
    def __init__(self, piece):
        super().__init__(piece)
        self.name = 'Night'
        self.set_target_types(['barrier'])
        self.confirm_message = "Consume this barrier?"
        self.highlight_types = ["highlight all targets"]

    def use_power(self, board, barriers):
        target_location = board.get_field(self.selected_barrier_1.location.x, self.selected_barrier_1.location.y)
        self.selected_barrier_1.remove_from_board(board, barriers)
        self.piece.move(target_location, board)

    def get_target_fields_1(self, board):
        target_fields = []

        adjacent_fields = self.piece.location.get_adjacent(board, type='all')
        for adjacent_field in adjacent_fields:
            if adjacent_field.barrier and adjacent_field.permitted_area_condition(self.piece):
                target_fields.append(adjacent_field)

        return target_fields

