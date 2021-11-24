# Evan Deutsch
# CS540
# 11/1/2020
import random
from copy import deepcopy

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        # TODO: detect drop phase
        # Done in successor function

        # TODO: implement a minimax algorithm to play better

        move = self.Max_Value(state, 0)[1]

        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and diamond wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][
                    col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # TODO: check \ diagonal wins
        for i in range(2):
            if state[i][i] != ' ' and state[i][i] == state[i + 1][i + 1] == state[i + 2][i + 2] == state[i + 3][i + 3]:
                return 1 if state[i][i] == self.my_piece else -1
            elif state[1 - i][i] != ' ' and state[1 - i][i] == state[2 - i][i + 1] == state[3 - i][i + 2] == \
                    state[4 - i][i + 3]:
                return 1 if state[1 - i][i] == self.my_piece else -1
        # TODO: check / diagonal wins
        for i in range(2):
            if state[i][4 - i] != ' ' and state[i][4 - i] == state[i + 1][3 - i] == state[i + 2][2 - i] == state[i + 3][
                1 - i]:
                return 1 if state[i][col] == self.my_piece else -1
            elif state[1 - i][4 - i] != ' ' and state[1 - i][4 - i] == state[2 - i][3 - i] == state[3 - i][2 - i] == \
                    state[4 - i][1 - i]:
                return 1 if state[i][col] == self.my_piece else -1
        # TODO: check diamond wins
        for i in range(3):
            for j in range(1, 4):
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j - 1] == state[i + 1][j + 1] == state[i + 2][j]:
                    return 1 if state[i][j] == self.my_piece else -1
        return 0  # no winner yet

    def heuristic_game_value(self, state):
        r_effective_touching_score = 1
        b_effective_touching_score = 1

        temp_value = self.game_value(state)
        if temp_value != 0:
            return temp_value
        else:
            prior_r_score = r_effective_touching_score
            # calculate r score
            # horizontal
            for row in state:
                for i in range(4):
                    if row[i] == 'r' and row[i] == row[i + 1]:
                        end = i + 1
                        temp_r_score = 2
                        if i < 3 and row[i] == row[i + 2]:
                            end = i + 2
                            temp_r_score += 1

                            if i < 2 and row[i + 3] == 'b':
                                temp_r_score -= 1

                        elif i < 3 and row[i + 2] == 'b':
                            temp_r_score -= 1

                        if i == 0 or end == 4:
                            temp_r_score -= 1

                        if i > 0 and row[i - 1] == 'b':
                            temp_r_score -= 1

                        if prior_r_score > 1 and temp_r_score > 1:
                            if prior_r_score > 2 or temp_r_score > 2:
                                temp_r_score = 4
                            else:
                                temp_r_score = 3

                        if r_effective_touching_score < temp_r_score:
                            r_effective_touching_score = temp_r_score

            # vertical
            prior_r_score = r_effective_touching_score
            for col in range(5):
                for i in range(4):
                    if state[i][col] == 'r' and state[i][col] == state[i + 1][col]:
                        end = i + 1
                        temp_r_score = 2

                        if i < 3 and state[i][col] == state[i + 2][col]:
                            end = i + 2
                            temp_r_score += 1

                            if i < 2 and state[i + 3][col] == 'b':
                                temp_r_score -= 1

                        elif i < 3 and state[i + 2][col] == 'b':
                            temp_r_score -= 1

                        if i == 0 or end == 4:
                            temp_r_score -= 1

                        if i > 0 and state[i - 1][col] == 'b':
                            temp_r_score -= 1

                        if prior_r_score > 1 and temp_r_score > 1:
                            if prior_r_score > 2 or temp_r_score > 2:
                                temp_r_score = 4
                            else:
                                temp_r_score = 3

                        if r_effective_touching_score < temp_r_score:
                            r_effective_touching_score = temp_r_score

            # diagonal \
            prior_r_score = r_effective_touching_score
            for i in range(4):
                if state[i][i] == 'r' and state[i][i] == state[i + 1][i + 1]:
                    end = i + 1
                    temp_r_score = 2

                    if i < 3 and state[i][i] == state[i + 2][i + 2]:
                        end = i + 2
                        temp_r_score += 1

                        if i < 2 and state[i + 3][i + 3] == 'b':
                            temp_r_score -= 1

                    elif i < 3 and state[i + 2][i + 2] == 'b':
                        temp_r_score -= 1

                    if i == 0 or end == 4:
                        temp_r_score -= 1

                    if i > 0 and state[i - 1][i - 1] == 'b':
                        temp_r_score -= 1

                    if prior_r_score > 1 and temp_r_score > 1:
                        if prior_r_score > 2 or temp_r_score > 2:
                            temp_r_score = 4
                        else:
                            temp_r_score = 3

                    if r_effective_touching_score < temp_r_score:
                        r_effective_touching_score = temp_r_score
            prior_r_score = r_effective_touching_score
            for i in range(3):
                if state[i][i + 1] == 'r' and state[i][i + 1] == state[i + 1][i + 2]:
                    end = i + 1
                    temp_r_score = 2

                    if i < 2 and state[i][i + 1] == state[i + 2][i + 3]:
                        end = i + 2
                        temp_r_score += 1

                        if i < 1 and state[i + 3][i + 4] == 'b':
                            temp_r_score -= 1

                    elif i < 2 and state[i + 2][i + 3] == 'b':
                        temp_r_score -= 1

                    if i == 0 or end == 3:
                        temp_r_score -= 1

                    if i > 0 and state[i - 1][i] == 'b':
                        temp_r_score -= 1

                    if prior_r_score > 1 and temp_r_score > 1:
                        if prior_r_score > 2 or temp_r_score > 2:
                            temp_r_score = 4
                        else:
                            temp_r_score = 3

                    if r_effective_touching_score < temp_r_score:
                        r_effective_touching_score = temp_r_score
            prior_r_score = r_effective_touching_score
            for i in range(3):
                if state[i + 1][i] == 'r' and state[i + 1][i] == state[i + 2][i + 1]:
                    end = i + 1
                    temp_r_score = 2

                    if i < 2 and state[i + 1][i] == state[i + 3][i + 2]:
                        end = i + 2
                        temp_r_score += 1

                        if i < 1 and state[i + 4][i + 3] == 'b':
                            temp_r_score -= 1

                    elif i < 2 and state[i + 3][i + 2] == 'b':
                        temp_r_score -= 1

                    if i == 0 or end == 3:
                        temp_r_score -= 1

                    if i > 0 and state[i][i - 1] == 'b':
                        temp_r_score -= 1

                    if prior_r_score > 1 and temp_r_score > 1:
                        if prior_r_score > 2 or temp_r_score > 2:
                            temp_r_score = 4
                        else:
                            temp_r_score = 3

                    if r_effective_touching_score < temp_r_score:
                        r_effective_touching_score = temp_r_score

            # diagonal /
            prior_r_score = r_effective_touching_score
            for i in range(4):
                if state[4 - i][i] == 'r' and state[4 - i][i] == state[3 - i][i + 1]:
                    end = i + 1
                    temp_r_score = 2

                    if i < 3 and state[4 - i][i] == state[2 - i][i + 2]:
                        end = i + 2
                        temp_r_score += 1

                        if i < 2 and state[1 - i][i + 3] == 'b':
                            temp_r_score -= 1

                    elif i < 2 and state[2 - i][i + 2] == 'b':
                        temp_r_score -= 1

                    if i == 0 or end == 4:
                        temp_r_score -= 1

                    if i > 0 and state[5 - i][i - 1] == 'b':
                        temp_r_score -= 1

                    if prior_r_score > 1 and temp_r_score > 1:
                        if prior_r_score > 2 or temp_r_score > 2:
                            temp_r_score = 4
                        else:
                            temp_r_score = 3

                    if r_effective_touching_score < temp_r_score:
                        r_effective_touching_score = temp_r_score
            prior_r_score = r_effective_touching_score
            for i in range(3):
                if state[4 - i][i + 1] == 'r' and state[4 - i][i + 1] == state[3 - i][i + 2]:
                    end = i + 1
                    temp_r_score = 2

                    if i < 2 and state[4 - i][i + 1] == state[2 - i][i + 3]:
                        end = i + 2
                        temp_r_score += 1

                        if i < 1 and state[1 - i][i + 4] == 'b':
                            temp_r_score -= 1

                    elif i < 2 and state[2 - i][i + 3] == 'b':
                        temp_r_score -= 1

                    if i == 0 or end == 3:
                        temp_r_score -= 1

                    if i > 0 and state[5 - i][i] == 'b':
                        temp_r_score -= 1

                    if prior_r_score > 1 and temp_r_score > 1:
                        if prior_r_score > 2 or temp_r_score > 2:
                            temp_r_score = 4
                        else:
                            temp_r_score = 3

                    if r_effective_touching_score < temp_r_score:
                        r_effective_touching_score = temp_r_score
            prior_r_score = r_effective_touching_score
            for i in range(3):
                if state[3 - i][i] == 'r' and state[3 - i][i] == state[2 - i][i + 1]:
                    end = i + 1
                    temp_r_score = 2

                    if i < 2 and state[3 - i][i] == state[1 - i][i + 2]:
                        end = i + 2
                        temp_r_score += 1

                        if i < 1 and state[i][i + 3] == 'b':
                            temp_r_score -= 1

                    elif i < 2 and state[1 - i][i + 2] == 'b':
                        temp_r_score -= 1

                    if i == 0 or end == 3:
                        temp_r_score -= 1

                    if i > 0 and state[4 - i][i - 1] == 'b':
                        temp_r_score -= 1

                    if prior_r_score > 1 and temp_r_score > 1:
                        if prior_r_score > 2 or temp_r_score > 2:
                            temp_r_score = 4
                        else:
                            temp_r_score = 3

                    if r_effective_touching_score < temp_r_score:
                        r_effective_touching_score = temp_r_score

            # diamond
            prior_r_score = r_effective_touching_score
            for i in range(3):
                for j in range(1, 4):
                    if (state[i][j] == 'r' and (
                            state[i][j] == state[i + 1][j - 1] == state[i + 1][j + 1] or state[i][j] == state[i + 1][
                        j - 1] == state[i + 2][j] or state[i][j] == state[i + 1][j + 1] == state[i + 2][j])) or (
                            state[i + 1][j + 1] == 'r' and state[i + 1][j + 1] == state[i + 1][j - 1] == state[i + 2][
                        j]):
                        temp_r_score = 2

                        if state[i][j] == 'b' or state[i + 1][j - 1] == 'b' or state[i + 1][j + 1] == 'b' or \
                                state[i + 2][j] == 'b':
                            temp_r_score -= 1

                        if prior_r_score > 1 and temp_r_score > 1:
                            if prior_r_score > 2 or temp_r_score > 2:
                                temp_r_score = 4
                            else:
                                temp_r_score = 3

                        if r_effective_touching_score < temp_r_score:
                            r_effective_touching_score = temp_r_score

            # calculate b score
            # horizontal
            prior_b_score = b_effective_touching_score
            for row in state:
                for i in range(4):
                    if row[i] == 'b' and row[i] == row[i + 1]:
                        end = i + 1
                        temp_b_score = 2

                        if i < 3 and row[i] == row[i + 2]:
                            end = i + 2
                            temp_b_score += 1

                            if i < 2 and row[i + 3] == 'r':
                                temp_b_score -= 1

                        elif i < 3 and row[i + 2] == 'r':
                            temp_b_score -= 1

                        if i == 0 or end == 4:
                            temp_b_score -= 1

                        if i > 0 and row[i - 1] == 'r':
                            temp_b_score -= 1

                        if prior_b_score > 1 and temp_b_score > 1:
                            if prior_b_score > 2 or temp_b_score > 2:
                                temp_b_score = 4
                            else:
                                temp_b_score = 3

                        if b_effective_touching_score < temp_b_score:
                            b_effective_touching_score = temp_b_score
            # vertical
            prior_b_score = b_effective_touching_score
            for col in range(5):
                for i in range(4):
                    if state[i][col] == 'b' and state[i][col] == state[i + 1][col]:
                        end = i + 1
                        temp_b_score = 2

                        if i < 3 and state[i][col] == state[i + 2][col]:
                            end = i + 2
                            temp_b_score += 1

                            if i < 2 and state[i + 3][col] == 'r':
                                temp_b_score -= 1

                        elif i < 3 and state[i + 2][col] == 'r':
                            temp_b_score -= 1

                        if i == 0 or end == 4:
                            temp_b_score -= 1

                        if i > 0 and state[i - 1][col] == 'r':
                            temp_b_score -= 1

                        if prior_b_score > 1 and temp_b_score > 1:
                            if prior_b_score > 2 or temp_b_score > 2:
                                temp_b_score = 4
                            else:
                                temp_b_score = 3

                        if b_effective_touching_score < temp_b_score:
                            b_effective_touching_score = temp_b_score

            # diagonal \
            prior_b_score = b_effective_touching_score
            for i in range(4):
                if state[i][i] == 'b' and state[i][i] == state[i + 1][i + 1]:
                    end = i + 1
                    temp_b_score = 2

                    if i < 3 and state[i][i] == state[i + 2][i + 2]:
                        end = i + 2
                        temp_b_score += 1

                        if i < 2 and state[i + 3][i + 3] == 'r':
                            temp_b_score -= 1

                    elif i < 3 and state[i + 2][i + 2] == 'r':
                        temp_b_score -= 1

                    if i == 0 or end == 4:
                        temp_b_score -= 1

                    if i > 0 and state[i - 1][i - 1] == 'r':
                        temp_b_score -= 1

                    if prior_b_score > 1 and temp_b_score > 1:
                        if prior_b_score > 2 or temp_b_score > 2:
                            temp_b_score = 4
                        else:
                            temp_b_score = 3

                    if b_effective_touching_score < temp_b_score:
                        b_effective_touching_score = temp_b_score
            prior_b_score = b_effective_touching_score
            for i in range(3):
                if state[i][i + 1] == 'b' and state[i][i + 1] == state[i + 1][i + 2]:
                    end = i + 1
                    temp_b_score = 2

                    if i < 2 and state[i][i + 1] == state[i + 2][i + 3]:
                        end = i + 2
                        temp_b_score += 1

                        if i < 1 and state[i + 3][i + 4] == 'r':
                            temp_b_score -= 1

                    elif i < 2 and state[i + 2][i + 3] == 'r':
                        temp_b_score -= 1

                    if i == 0 or end == 3:
                        temp_b_score -= 1

                    if i > 0 and state[i - 1][i] == 'r':
                        temp_b_score -= 1

                    if prior_b_score > 1 and temp_b_score > 1:
                        if prior_b_score > 2 or temp_b_score > 2:
                            temp_b_score = 4
                        else:
                            temp_b_score = 3

                    if b_effective_touching_score < temp_b_score:
                        b_effective_touching_score = temp_b_score
            prior_b_score = b_effective_touching_score
            for i in range(3):
                if state[i + 1][i] == 'b' and state[i + 1][i] == state[i + 2][i + 1]:
                    end = i + 1
                    temp_b_score = 2

                    if i < 2 and state[i + 1][i] == state[i + 3][i + 2]:
                        end = i + 2
                        temp_b_score += 1

                        if i < 1 and state[i + 4][i + 3] == 'r':
                            temp_b_score -= 1

                    elif i < 2 and state[i + 3][i + 2] == 'r':
                        temp_b_score -= 1

                    if i == 0 or end == 3:
                        temp_b_score -= 1

                    if i > 0 and state[i][i - 1] == 'r':
                        temp_b_score -= 1

                    if prior_b_score > 1 and temp_b_score > 1:
                        if prior_b_score > 2 or temp_b_score > 2:
                            temp_b_score = 4
                        else:
                            temp_b_score = 3

                    if b_effective_touching_score < temp_b_score:
                        b_effective_touching_score = temp_b_score

            # diagonal /
            prior_b_score = b_effective_touching_score
            for i in range(4):
                if state[4 - i][i] == 'b' and state[4 - i][i] == state[3 - i][i + 1]:
                    end = i + 1
                    temp_b_score = 2

                    if i < 3 and state[4 - i][i] == state[2 - i][i + 2]:
                        end = i + 2
                        temp_b_score += 1

                        if i < 2 and state[1 - i][i + 3] == 'r':
                            temp_b_score -= 1

                    elif i < 3 and state[2 - i][i + 2] == 'r':
                        temp_b_score -= 1

                    if i == 0 or end == 4:
                        temp_b_score -= 1

                    if i > 0 and state[5 - i][i - 1] == 'r':
                        temp_b_score -= 1

                    if prior_b_score > 1 and temp_b_score > 1:
                        if prior_b_score > 2 or temp_b_score > 2:
                            temp_b_score = 4
                        else:
                            temp_b_score = 3

                    if b_effective_touching_score < temp_b_score:
                        b_effective_touching_score = temp_b_score
            prior_b_score = b_effective_touching_score
            for i in range(3):
                if state[4 - i][i + 1] == 'b' and state[4 - i][i + 1] == state[3 - i][i + 2]:
                    end = i + 1
                    temp_b_score = 2

                    if i < 2 and state[4 - i][i + 1] == state[2 - i][i + 3]:
                        end = i + 2
                        temp_b_score += 1

                        if i < 1 and state[1 - i][i + 4] == 'r':
                            temp_b_score -= 1

                    elif i < 2 and state[2 - i][i + 3] == 'r':
                        temp_b_score -= 1

                    if i == 0 or end == 3:
                        temp_b_score -= 1

                    if i > 0 and state[5 - i][i] == 'r':
                        temp_b_score -= 1

                    if prior_b_score > 1 and temp_b_score > 1:
                        if prior_b_score > 2 or temp_b_score > 2:
                            temp_b_score = 4
                        else:
                            temp_b_score = 3

                    if b_effective_touching_score < temp_b_score:
                        b_effective_touching_score = temp_b_score
            prior_b_score = b_effective_touching_score
            for i in range(3):
                if state[3 - i][i] == 'b' and state[3 - i][i] == state[2 - i][i + 1]:
                    end = i + 1
                    temp_b_score = 2

                    if i < 2 and state[3 - i][i] == state[1 - i][i + 2]:
                        end = i + 2
                        temp_b_score += 1

                        if i < 1 and state[i][i + 3] == 'r':
                            temp_b_score -= 1

                    elif i < 2 and state[1 - i][i + 2] == 'r':
                        temp_b_score -= 1

                    if i == 0 or end == 3:
                        temp_b_score -= 1

                    if i > 0 and state[4 - i][i - 1] == 'r':
                        temp_b_score -= 1

                    if prior_b_score > 1 and temp_b_score > 1:
                        if prior_b_score > 2 or temp_b_score > 2:
                            temp_b_score = 4
                        else:
                            temp_b_score = 3

                    if b_effective_touching_score < temp_b_score:
                        b_effective_touching_score = temp_b_score

            # diamond
            prior_b_score = b_effective_touching_score
            for i in range(3):
                for j in range(1, 4):
                    if (state[i][j] == 'b' and (
                            state[i][j] == state[i + 1][j - 1] == state[i + 1][j + 1] or state[i][j] == state[i + 1][
                        j - 1] == state[i + 2][j] or state[i][j] == state[i + 1][j + 1] == state[i + 2][j])) or (
                            state[i + 1][j + 1] == 'b' and state[i + 1][j + 1] == state[i + 1][j - 1] == state[i + 2][
                        j]):
                        temp_b_score = 2

                        if state[i][j] == 'r' or state[i + 1][j - 1] == 'r' or state[i + 1][j + 1] == 'r' or \
                                state[i + 2][j] == 'r':
                            temp_b_score -= 1

                        if prior_b_score > 1 and temp_b_score > 1:
                            if prior_b_score > 2 or temp_b_score > 2:
                                temp_b_score = 4
                            else:
                                temp_b_score = 3

                        if b_effective_touching_score < temp_b_score:
                            b_effective_touching_score = temp_b_score

        heurstic_game_value = 0
        if r_effective_touching_score > b_effective_touching_score:
            heurstic_game_value = float(b_effective_touching_score) / float(r_effective_touching_score)
            if self.my_piece == 'b':
                heurstic_game_value = -(1 - heurstic_game_value)
            else:
                heurstic_game_value = 1 - heurstic_game_value
        else:
            heurstic_game_value = float(r_effective_touching_score) / float(b_effective_touching_score)
            if self.my_piece == 'r':
                heurstic_game_value = -(1 - heurstic_game_value)
            else:
                heurstic_game_value = 1 - heurstic_game_value

        return heurstic_game_value

    def Max_Value(self, state, depth):
        successor_dict = {
            0: (-1, -1),
            1: (-1, 0),
            2: (-1, 1),
            3: (0, -1),
            4: (0, 1),
            5: (1, -1),
            6: (1, 0),
            7: (1, 1),
        }
        current_value = self.heuristic_game_value(state)

        if current_value == 1 or current_value == -1:
            return current_value, []
        if depth == 3:
            return current_value, []
        alpha = -1.5
        successor_values = self.my_succ(state)
        successors = successor_values[0]
        m_values = successor_values[1]
        count = 0
        best_count = -1
        for s in successors:
            temp_alpha = self.Min_Value(s, depth + 1)
            if temp_alpha > alpha:
                alpha = temp_alpha
                best_count = count
            count += 1
        index_i = -1
        index_j = -1
        for i in range(5):
            for j in range(5):
                if self.drop_phase(state, self.my_piece) and state[i][j] != successors[best_count][i][j]:
                    index_i = i
                    index_j = j
                    break
                elif state[i][j] == self.my_piece and successors[best_count][i][j] != self.my_piece:
                    index_i = i
                    index_j = j
                    break
        if m_values != 0:
            return alpha, [(index_i + successor_dict[m_values[best_count]][0], index_j + successor_dict[m_values[best_count]][1]), (index_i, index_j)]
        return alpha, [(index_i, index_j)]

    def Min_Value(self, state, depth):
        current_value = self.heuristic_game_value(state)

        if current_value == 1 or current_value == -1:
            return current_value
        if depth == 3:
            return current_value
        beta = 1.5
        successors = self.opponent_succ(state)[0]
        for s in successors:
            temp_beta = float(self.Max_Value(s, depth + 1)[0])
            temp_beta -= 0.0001
            if temp_beta < beta:
                beta = temp_beta
        return beta

    def my_succ(self, state):
        successors = []
        m_values = []
        successor_dict = {
            0: (-1, -1),
            1: (-1, 0),
            2: (-1, 1),
            3: (0, -1),
            4: (0, 1),
            5: (1, -1),
            6: (1, 0),
            7: (1, 1),
        }
        if self.drop_phase(state, self.my_piece):
            for i in range(5):
                for j in range(5):
                    temp_state = deepcopy(state)
                    if temp_state[i][j] == ' ':
                        temp_state[i][j] = self.my_piece
                        successors.append(temp_state)
            return successors, 0
        for i in range(5):
            for j in range(5):
                temp_state = deepcopy(state)
                if temp_state[i][j] == self.my_piece:
                    temp_state[i][j] = ' '
                    for m in range(8):
                        tup = successor_dict[m]
                        a = tup[0]
                        b = tup[1]
                        if 0 <= i + a < 5 and 0 <= j + b < 5 and temp_state[i + a][j + b] == ' ':
                            temp_state_2 = deepcopy(temp_state)
                            temp_state_2[i + a][j + b] = self.my_piece
                            successors.append(temp_state_2)
                            m_values.append(m)
                            temp_state[i + a][j + b] = ' '
        return (successors, m_values)

    def opponent_succ(self, state):
        opponent_piece = ' '
        if self.my_piece == 'r':
            opponent_piece = 'b'
        else:
            opponent_piece = 'r'
        successors = []
        m_values = []
        successor_dict = {
            0: (-1, -1),
            1: (-1, 0),
            2: (-1, 1),
            3: (0, -1),
            4: (0, 1),
            5: (1, -1),
            6: (1, 0),
            7: (1, 1),
        }
        if self.drop_phase(state, opponent_piece):
            for i in range(5):
                for j in range(5):
                    temp_state = deepcopy(state)
                    if temp_state[i][j] == ' ':
                        temp_state[i][j] = opponent_piece
                        successors.append(temp_state)
            return successors, 0
        for i in range(5):
            for j in range(5):
                temp_state = deepcopy(state)
                if temp_state[i][j] == opponent_piece:
                    temp_state[i][j] = ' '
                    for m in range(8):
                        tup = successor_dict[m]
                        a = tup[0]
                        b = tup[1]
                        if 0 <= i + a < 5 and 0 <= j + b < 5 and temp_state[i + a][j + b] == ' ':
                            temp_state_2 = deepcopy(temp_state)
                            temp_state_2[i + a][j + b] = opponent_piece
                            successors.append(temp_state_2)
                            m_values.append(m)
                            temp_state[i + a][j + b] = ' '
        return (successors, m_values)

    def drop_phase(self, state, piece):
        piece_count = 0

        for i in range(5):
            for j in range(5):
                if state[i][j] == piece:
                    piece_count += 1
        if piece_count == 4:
            return False
        return True



############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
