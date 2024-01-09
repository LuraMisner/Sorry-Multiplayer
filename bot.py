import constants
import random
import time
from board import Board
from card_value import Value
from reserved_type import ReservedType


class Bot:
    def __init__(self, color):
        # Information needed to be in line with the player class
        self.color = color
        self.safety_start = constants.SAFETY_STARTS[self.color]
        self.home = constants.HOMES[self.color]
        self.start = constants.STARTS[self.color]
        self.slides = constants.SLIDES[self.color]
        self.positions = [constants.STARTS[self.color]] * 4

        # Needed to calculate moves
        self.all_positions = {}
        self.board = Board()

    def get_color(self):
        return self.color

    def get_positions(self):
        return self.positions

    def get_safety_start(self):
        return self.safety_start

    def get_home(self):
        return self.home

    def get_start(self):
        return self.start

    def get_slides(self):
        return self.slides

    def update_position(self, index, new_position):
        self.positions[index] = new_position

    def update_positions(self, new_positions):
        self.positions = new_positions

    def handle_turn(self, all_positions, card) -> {str: [int]}:
        print(self.color, card.get_value())
        # Update positions
        self.all_positions = all_positions
        self.update_positions(self.all_positions[self.color])

        # Loop through and check which piece has a valid move, selected at random
        valid_move = False
        pos = self.positions.copy()
        while not valid_move and not len(pos) == 0:
            # Select a start position at random
            start_pos = pos.pop(random.randint(0, len(pos) - 1))
            possible_moves = self.calculate_end_positions(start_pos, card)

            # If there is a possible move, select it at random and update positions
            if possible_moves != {}:
                move, end_pos = random.choice(list(possible_moves.items()))
                print(move, end_pos)

                # Handle an 11 swap
                if move == 'swap' and card.get_value() == Value.Eleven:
                    index = self.positions.index(start_pos)
                    # Find the player that is being swapped
                    for p_colors in self.all_positions.keys():
                        if p_colors != self.color:
                            if end_pos in self.all_positions[p_colors]:
                                ind = self.all_positions[p_colors].index(end_pos)

                                # Update the value for both
                                self.all_positions[p_colors][ind] = start_pos
                                self.all_positions[self.color][index] = end_pos

                    valid_move = True

                # Handle seven split
                elif 'split' in possible_moves and possible_moves['split'] == 0:
                    # If there was a valid split, then everything is handled end the turn here
                    valid_move = True

                # Make sure that we don't already occupy this spot.
                elif not self.check_occupied_by_us(end_pos):
                    index = self.positions.index(start_pos)
                    self.all_positions[self.color][index] = end_pos

                    # Handle slide or occupied
                    self.all_positions[self.color][index] = self.check_slide(end_pos, index)
                    self.check_occupied(self.all_positions[self.color][index], index)
                    valid_move = True

        # Returns the positions back to the server
        time.sleep(1.5)
        self.update_positions(self.all_positions[self.color])
        print("bot returns this", self.all_positions)
        return self.all_positions

    def check_occupied_by_us(self, position) -> bool:
        """
        Check if our piece already occupies a spot
        :param position: Integer, id of space
        :return: Boolean
        """
        for pos in self.positions:
            if position == pos:
                return True

        return False

    def check_occupied(self, space_id, index):
        """
        Checks if a space is already occupied by another player, and handles the necessary adjustments to positions
        for sending them back to start.
        :param space_id: Integer of the space ID
        :param index: Index of the piece that is being moved there
        """

        for key in self.all_positions.keys():
            if key != self.color:
                if space_id in self.all_positions[key]:
                    ind = self.all_positions[key].index(space_id)

                    # Need to move the player back to their spawn
                    self.all_positions[key][ind] = constants.STARTS[key]

            else:
                # Need to make sure you aren't counting the one that just moved, or any in the home
                for ind, space in enumerate(self.all_positions[self.color]):
                    if space == space_id and ind != index and space_id != constants.HOMES[self.color]:
                        self.all_positions[self.color][ind] = constants.STARTS[self.color]

    def check_slide(self, start_pos, piece_id) -> int:
        """
        Checks if the end position is the start of a slide, and updates the position accordingly
        :param start_pos: Integer of start position
        :param piece_id: Integer representing the id of the piece
        :return: Integer representing the end position
        """
        space_value = self.board.board[start_pos].get_type().value
        if 'Slide' not in space_value:
            return start_pos

        # Can't take your own slide
        elif self.color in space_value:
            return start_pos

        else:
            # Calculate the end position
            for key in constants.SLIDES.keys():
                for slide in constants.SLIDES[key]:
                    s, e = slide

                    if s == start_pos:
                        # Go through the entirety of the slide if we are sliding anyone off it
                        s_ind = self.board.inorder_mapping.index(s)
                        e_ind = self.board.inorder_mapping.index(e)

                        for i in range(s_ind, e_ind + 1):
                            s_id = self.board.inorder_mapping[i]
                            if 'Slide' in self.board.board[s_id].get_type().value:
                                self.check_occupied(self.board.inorder_mapping[i], piece_id)

                        return e
        return start_pos

    def calculate_end_positions(self, start_pos, card) -> {str: int}:
        """
        Main function for calculating end positions for each card
        :param start_pos: Integer representing the starting position
        :param card: Card object representing the card drawn
        :return: Dictionary mapping a name to the end position {str : int} for every possible move
        """
        possible_moves = {}
        val = card.get_value()

        # Start position is home, there should be no movements ever.
        if start_pos == constants.HOMES[self.color]:
            return possible_moves

        # One or Two
        if val == Value.One or val == Value.Two:
            if start_pos == constants.STARTS[self.color]:
                possible_moves['start'] = self.board.inorder_mapping[self.board.inorder_mapping.index(start_pos) - 1]
            else:
                if val == Value.One:
                    end_pos = self.calculate_forward_position(start_pos, 1)
                    if not end_pos == -1:
                        possible_moves['forward'] = end_pos
                else:
                    end_pos = self.calculate_forward_position(start_pos, 2)
                    if not end_pos == -1:
                        possible_moves['forward'] = end_pos

        # Three
        elif val == Value.Three:
            end_pos = self.calculate_forward_position(start_pos, 3)
            if not end_pos == -1:
                possible_moves['forward'] = end_pos

        # Four
        elif val == Value.Four:
            end_pos = self.calculate_backward_position(start_pos, 4)
            if not end_pos == -1:
                possible_moves['backward'] = end_pos

        # Five
        elif val == Value.Five:
            end_pos = self.calculate_forward_position(start_pos, 5)
            if not end_pos == -1:
                possible_moves['forward'] = end_pos

        # Seven
        elif val == Value.Seven:
            end_pos = self.calculate_forward_position(start_pos, 7)
            if not end_pos == -1:
                possible_moves['forward'] = end_pos

            possible = self.check_split_possible()
            if possible and start_pos != constants.STARTS[self.color] and start_pos != constants.HOMES[self.color]:
                self.all_positions[self.color], value = self.handle_split()
                possible_moves['split'] = value
                print(self.all_positions)

        # Eight
        elif val == Value.Eight:
            end_pos = self.calculate_forward_position(start_pos, 8)
            if not end_pos == -1:
                possible_moves['forward'] = end_pos

        # Ten
        elif val == Value.Ten:
            end_pos = self.calculate_forward_position(start_pos, 10)
            if not end_pos == -1:
                possible_moves['forward'] = end_pos

            end_pos = self.calculate_backward_position(start_pos, 1)
            if not end_pos == -1:
                possible_moves['backward'] = end_pos

        # Eleven
        elif val == Value.Eleven:
            end_pos = self.calculate_forward_position(start_pos, 11)
            if not end_pos == -1:
                possible_moves['forward'] = end_pos

            if start_pos != constants.STARTS[self.color] and \
                    'Safety' not in self.board.board[start_pos].get_type().value:
                end_pos = self.calculate_swap_position()
                if len(end_pos) > 0:
                    possible_moves['swap'] = end_pos[random.randint(0, len(end_pos) - 1)]

        # Twelve:
        elif val == Value.Twelve:
            end_pos = self.calculate_forward_position(start_pos, 12)
            if not end_pos == -1:
                possible_moves['forward'] = end_pos

        # Sorry
        elif val == Value.Sorry:
            if start_pos == constants.STARTS[self.color]:
                end_pos = self.calculate_swap_position()
                if len(end_pos) > 0:
                    possible_moves['swap'] = end_pos[random.randint(0, len(end_pos) - 1)]

        return possible_moves

    def calculate_forward_position(self, start_pos, moves) -> int:
        """
        Calculates the end position of a player moving forward
        :param start_pos: Integer representing the start position
        :param moves: Integer representing how many steps forward
        :return: Integer representing the players end position
        """

        space_type = self.board.board[start_pos].get_type()

        # If this piece is not one that can be moved forward
        if space_type == ReservedType.START or space_type == ReservedType.HOME:
            return -1

        # Otherwise check that it can be moved the amount of spaces. If it reaches Home before then, it can't.
        space_ind = self.board.inorder_mapping.index(start_pos)

        while moves > 0:
            space_ind = (space_ind + 1) % len(self.board.inorder_mapping)
            space_type = self.board.board[self.board.inorder_mapping[space_ind]].get_type()

            if self.board.inorder_mapping[space_ind] == constants.HOMES[self.color]:
                if moves != 1:
                    return -1
                moves -= 1

            # If this isn't a start/home or other colors safety then decrease the moves
            elif space_type != ReservedType.HOME and space_type != ReservedType.START and \
                    self.check_other_safety(self.board.inorder_mapping[space_ind]):
                moves -= 1

        return self.board.inorder_mapping[space_ind]

    def check_other_safety(self, space_id) -> bool:
        """
        Checks if a space is another players safety/home so that it can be skipped over when moving around the board
        :param space_id: Integer representing the ID of the space
        :return: Boolean of whether this space should be counted while moving
        """
        space_type = self.board.board[space_id].get_type()

        if (self.color == 'Green' and space_type == ReservedType.GREEN_SAFETY) or \
                (self.color == 'Red' and space_type == ReservedType.RED_SAFETY) or \
                (self.color == 'Blue' and space_type == ReservedType.BLUE_SAFETY) or \
                (self.color == 'Yellow' and space_type == ReservedType.YELLOW_SAFETY):
            return True

        elif 'Safety' not in space_type.value:
            return True

        return False

    def calculate_backward_position(self, start_pos, moves) -> int:
        """
        Calculates the end position of a user moving backwards
        :param start_pos: Integer of the start ID
        :param moves: Integer representing how many moves backwards
        :return: Integer representing the end position
        """
        space_type = self.board.board[start_pos].get_type()

        # If this piece is not one that can be moved forward
        if space_type == ReservedType.START or space_type == ReservedType.HOME:
            return -1

        # Otherwise check that it can be moved the amount of spaces. If it reaches Home before then, it can't.
        space_ind = self.board.inorder_mapping.index(start_pos)

        while moves > 0:
            space_ind = (space_ind - 1) % len(self.board.inorder_mapping)
            space_type = self.board.board[self.board.inorder_mapping[space_ind]].get_type()

            # If this isn't a start/home or other colors safety then decrease the moves
            if space_type != ReservedType.HOME and space_type != ReservedType.START and \
                    self.check_other_safety(self.board.inorder_mapping[space_ind]):
                # If you are in safety then back out of the safety, otherwise skip over safety strip
                if 'Safety' in self.board.board[start_pos].get_type().value:
                    moves -= 1
                elif 'Safety' not in space_type.value:
                    moves -= 1

        return self.board.inorder_mapping[space_ind]

    def calculate_swap_position(self) -> [int]:
        """
        Finds all possible end positions that a user can swap with.
        :return: Array of Integers representing the ID of the end positions
        """
        # Find the end positions
        end_positions = []
        for key in self.all_positions.keys():
            if key != self.color:
                for item in self.all_positions[key]:
                    # If the player is not in a start, home, or safety zone then they may swap
                    space_type = self.board.board[item].get_type()
                    if space_type != ReservedType.HOME and space_type != ReservedType.START and \
                            'Safety' not in space_type.value:
                        end_positions.append(item)

        return end_positions

    def pick_swap(self) -> int:
        """
        Allows bot to randomly select a swap
        :return: Integer representing the id of the space selected
        """
        possible_swaps = self.calculate_swap_position()

        # Only one solution
        if len(possible_swaps) == 1:
            return possible_swaps[0]

        return possible_swaps[random.randint(0, len(possible_swaps) - 1)]

    def check_forward(self) -> [int]:
        """
        Calculate how many moves forward the pieces can go for the 7 split
        :return: array of integers
        """
        results = []

        # Find the largest amount of steps each piece can take.
        for p in self.all_positions[self.color]:
            if p == constants.STARTS[self.color] or p == constants.HOMES[self.color]:
                results.append(0)
            else:
                flag = False
                for i in range(6, -1, -1):
                    if not flag and self.calculate_forward_position(p, i) != -1:
                        results.append(i)
                        flag = True

        return results

    def check_split_possible(self) -> bool:
        """
        Checks if there is at least 2 pieces that can be moved a combined 7 spaces
        :return: Boolean
        """
        results = self.check_forward()
        results.sort()

        # If any two add up to 7 or more, then return True
        if results[2] + results[3] >= 7:
            return True
        return False

    def draw_split_positions(self, ind, max_moves) -> int:
        """
        :param ind: Piece index
        :param max_moves: Maximum number of moves they can make
        :return: Integer, how many spaces the piece moved
        """
        end_pos = []
        moves = []
        results = self.check_forward()

        # Highlight all possible end locations for the piece
        for i in range(1, max_moves + 1):
            end_position = self.calculate_forward_position(self.all_positions[self.color][ind], i)

            # Make sure there is another piece that can be moved the remaining spaces
            flag = False
            for n in range(len(results)):
                if n != ind and results[n] >= (7 - i):
                    flag = True

            if end_position != -1 and flag:
                end_pos.append(end_position)
                moves.append(i)

        if len(moves) > 0:
            return moves[random.randint(0, len(moves) - 1)]
        else:
            return -1

    def handle_split(self) -> ([int], int):
        """
        Main function for selecting the pieces and moves being made from the 7 split
        :return: Array of Integers, representing the new positions of the pieces
        """
        positions = self.all_positions[self.color]
        max_moves = 7

        indexes = [0, 1, 2, 3]
        first_move = -1

        while len(indexes) > 0 and first_move == -1:
            # randomly pick a piece and see how it can move forward
            ind = indexes.pop(random.randint(0, len(indexes)-1))
            first_move = self.draw_split_positions(ind, max_moves)

            # If there is a valid move, update the positions
            if first_move != -1:
                # Update the position
                positions[ind] = self.calculate_forward_position(positions[ind], first_move)
                positions[ind] = self.check_slide(positions[ind], ind)
                self.check_occupied(positions[ind], ind)

        # If we hit this, there are no possible moves, return the positions untouched
        if first_move == -1:
            return positions, -1

        # If there is a second move to be made, then make it
        max_moves -= first_move
        if max_moves > 0:
            # Go through the list of indexes and see which can move forward max_moves
            second_move_made = False
            indexes = [0, 1, 2, 3]

            while len(indexes) > 0 and not second_move_made:
                i = indexes.pop(random.randint(0, len(indexes) - 1))
                end_pos = self.calculate_forward_position(positions[i], max_moves)

                if end_pos != -1:
                    # Make the move and update the position
                    positions[i] = end_pos
                    positions[i] = self.check_slide(positions[i], i)
                    self.check_occupied(positions[i], i)
                    second_move_made = True

        return positions, 0
