from board import Board
import constants
from card_value import Value
from images import Images
from network import Network
import pygame
from reserved_type import ReservedType
import time
from card import Card


# noinspection PyTypeChecker
class Client:
    def __init__(self, win):
        self.window = win
        self.board = Board(self.window)
        self.network = Network()

        self.player = None

        self.char_select_group = pygame.sprite.Group()
        self.rules = pygame.sprite.Group()
        self.initialize_image_groups()

    def initialize_image_groups(self):
        title = Images(500, 175, 'images/start_screen/sorry_title.png')
        self.char_select_group.add(title)

        selection = Images(375, 330, 'images/start_screen/selected.png')
        self.char_select_group.add(selection)

        green = Images(215, 5, 'images/start_screen/green.png')
        self.char_select_group.add(green)

        red = Images(875, 5, 'images/start_screen/red.png')
        self.char_select_group.add(red)

        yellow = Images(215, 670, 'images/start_screen/yellow.png')
        self.char_select_group.add(yellow)

        blue = Images(875, 670, 'images/start_screen/blue.png')
        self.char_select_group.add(blue)

        confirm = Images(550, 400, 'images/start_screen/confirm.png')
        self.char_select_group.add(confirm)

        self.rules.add(Images(1000, 0, 'images/titles/rules.png'))

    def get_server_response(self, query):
        return self.network.send(query)

    def select_color(self):
        selected = False
        choice = None
        select_group = pygame.sprite.Group()

        while not selected:
            # Draw out the colors
            self.draw_box(0, 0, constants.SELECT_X, constants.SELECT_Y, constants.GREEN, constants.BLACK)
            self.draw_box(650, 0, constants.SELECT_X, constants.SELECT_Y, constants.RED, constants.BLACK)
            self.draw_box(0, 375, constants.SELECT_X, constants.SELECT_Y, constants.YELLOW, constants.BLACK)
            self.draw_box(650, 375, constants.SELECT_X, constants.SELECT_Y, constants.BLUE, constants.BLACK)

            # If a color is no longer available, then grey it out
            available_colors = self.get_server_response('available_colors')
            if 'Green' not in available_colors:
                self.draw_transparent_box(0, 0, constants.SELECT_X, constants.SELECT_Y)
            if 'Red' not in available_colors:
                self.draw_transparent_box(650, 0, constants.SELECT_X, constants.SELECT_Y)
            if 'Yellow' not in available_colors:
                self.draw_transparent_box(0, 375, constants.SELECT_X, constants.SELECT_Y)
            if 'Blue' not in available_colors:
                self.draw_transparent_box(650, 375, constants.SELECT_X, constants.SELECT_Y)

            # Display the number ready
            rdy = self.get_server_response('num_ready')
            self.draw_text(f'{rdy[1]} / {rdy[0]} players ready', 24, constants.WHITE, 575, 450)

            # Look for a selection
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                    if 550 <= x <= 550 + constants.CONFIRM_X and 400 <= y <= 400 + constants.CONFIRM_Y:
                        if choice:
                            selected = True
                    elif 0 <= x <= constants.SELECT_X and 0 <= y <= constants.SELECT_Y:
                        choice = 'Green'
                        select_group.empty()
                        select_group.add(Images(650, 326, 'images/start_screen/green_small.png'))
                    elif 650 <= x <= 650 + constants.SELECT_X and 0 <= y <= constants.SELECT_Y:
                        choice = 'Red'
                        select_group.empty()
                        select_group.add(Images(640, 325, 'images/start_screen/red_small.png'))
                    elif 0 <= x <= constants.SELECT_X and 375 <= y <= 375 + constants.SELECT_Y:
                        choice = 'Yellow'
                        select_group.empty()
                        select_group.add(Images(655, 325, 'images/start_screen/yellow_small.png'))
                    elif 650 <= x <= 650 + constants.SELECT_X and 375 <= y <= 375 + constants.SELECT_Y:
                        choice = 'Blue'
                        select_group.empty()
                        select_group.add(Images(650, 325, 'images/start_screen/blue_small.png'))

            # Wait for a selection
            self.char_select_group.draw(self.window)
            select_group.draw(self.window)
            pygame.display.update()

        # Verify the selection with the server, if not verified recall the function
        verified = self.get_server_response(f'verify_choice {choice}')
        if not verified:
            return self.select_color()
        else:
            self.player = self.get_server_response('my_player')
            return self.wait_for_start()

    def wait_for_start(self):
        start = self.get_server_response('start')

        while not start:
            rdy = self.get_server_response('num_ready')

            self.draw_box(1, 450, constants.SELECT_X-2, 20, constants.YELLOW, constants.YELLOW)
            self.draw_box(501, 450, 100, 20, constants.BLUE, constants.BLUE)

            self.draw_text(f'{rdy[1]} / {rdy[0]} players ready', 24, constants.WHITE, 425, 450)
            pygame.display.flip()

            start = self.get_server_response('start')

    def draw_box(self, x, y, x_length, y_length, color, outline):
        """
        Draws a box on the window
        :param x: Integer, x position of top left corner
        :param y: Integer, y position of top left corner
        :param x_length: Integer, length
        :param y_length: Integer, height
        :param color: (int, int, int), color of box
        :param outline: (int, int, int), color of outline
        """

        background = pygame.Rect(x, y, x_length, y_length)
        pygame.draw.rect(self.window, outline, background)
        rect = pygame.Rect(x + 2, y + 2, x_length - 4, y_length - 4)
        pygame.draw.rect(self.window, color, rect)

    def draw_transparent_box(self, x, y, width, height):
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.window.blit(s, (x, y))

    def draw_text(self, text, size, color, x, y):
        """
        Draws a text object on the window
        :param text: String, text being displayed
        :param size: Integer, size of the text
        :param color: (int, int, int), color of the text
        :param x: Integer, x position of top left corner
        :param y: Integer, y position of top left corner
        """
        font = pygame.font.SysFont('freesansbold.ttf', size)
        self.window.blit(font.render(text, True, color), (x, y))

    def draw_players(self):
        player_positions = self.get_server_response('get_player_positions')
        print(player_positions)

        for player in player_positions.keys():
            for ind, piece in enumerate(player_positions[player]):
                # Draw it
                if player == 'Green':
                    color = constants.GREEN
                elif player == 'Red':
                    color = constants.RED
                elif player == 'Yellow':
                    color = constants.YELLOW
                else:
                    color = constants.BLUE

                x = constants.BOARD_SQUARE * (piece // 16)
                y = constants.BOARD_SQUARE * (piece % 16)
                center_y = x + (constants.BOARD_SQUARE // 2)
                center_x = y + (constants.BOARD_SQUARE // 2)

                pygame.draw.circle(self.window, constants.BLACK, (center_x, center_y),
                                   (constants.BOARD_SQUARE // 2.5) + 2.5)
                pygame.draw.circle(self.window, color, (center_x, center_y), constants.BOARD_SQUARE // 2.5)

                # label piece
                self.draw_text(str(ind + 1), 30, constants.BLACK, center_x - 7, x + 13)

    def draw_screen(self):
        self.window.fill(constants.BACKGROUND)
        self.board.draw_board()
        self.draw_players()
        self.draw_card()
        self.draw_turn()
        self.rules.draw(self.window)
        pygame.display.update()

    def draw_card(self):
        card_group = pygame.sprite.Group()
        card = self.get_server_response('get_card')
        if card:
            val = card.get_value()

            if val == Value.One:
                card_group.add(Images(275, 225, 'images/cards/one.png'))
            elif val == Value.Two:
                card_group.add(Images(275, 225, 'images/cards/two.png'))
            elif val == Value.Three:
                card_group.add(Images(275, 225, 'images/cards/three.png'))
            elif val == Value.Four:
                card_group.add(Images(275, 225, 'images/cards/four.png'))
            elif val == Value.Five:
                card_group.add(Images(275, 225, 'images/cards/five.png'))
            elif val == Value.Seven:
                card_group.add(Images(275, 225, 'images/cards/seven.png'))
            elif val == Value.Eight:
                card_group.add(Images(275, 225, 'images/cards/eight.png'))
            elif val == Value.Ten:
                card_group.add(Images(275, 225, 'images/cards/ten.png'))
            elif val == Value.Eleven:
                card_group.add(Images(275, 225, 'images/cards/eleven.png'))
            elif val == Value.Twelve:
                card_group.add(Images(275, 225, 'images/cards/twelve.png'))
            else:
                card_group.add(Images(275, 225, 'images/cards/sorry.png'))

            card_group.draw(self.window)

    def draw_turn(self):
        color = self.get_server_response('whos_turn')
        title_group = pygame.sprite.Group()

        if color == self.player.get_color():
            if color == 'Green':
                title_group.add(Images(722, 10, 'images/titles/you_green.png'))
            elif color == 'Blue':
                title_group.add(Images(722, 10, 'images/titles/you_blue.png'))
            elif color == 'Red':
                title_group.add(Images(722, 10, 'images/titles/you_red.png'))
            else:
                title_group.add(Images(722, 10, 'images/titles/you_yellow.png'))
        elif color == 'Green':
            title_group.add(Images(722, 10, 'images/titles/green.png'))
        elif color == 'Red':
            title_group.add(Images(722, 10, 'images/titles/red.png'))
        elif color == 'Blue':
            title_group.add(Images(722, 10, 'images/titles/blue.png'))
        else:
            title_group.add(Images(722, 10, 'images/titles/yellow.png'))

        title_group.draw(self.window)

    def check_our_turn(self):
        reply = self.get_server_response('whos_turn')
        if reply == self.player.get_color():
            self.handle_turn()

    def handle_turn(self):
        self.get_server_response('draw_card')
        self.handle_movement(self.get_server_response('get_card'))

        self.get_server_response('end_turn')

    def handle_movement(self, card):
        self.draw_screen()
        movement_group = pygame.sprite.Group()
        movement_group.add(Images(750, 75, 'images/movement/select_piece.png'))
        movement_group.draw(self.window)
        pygame.display.update()

        card = Card(Value.One)
        val = card.get_value()
        piece_id = self.select_piece()
        possible_moves = self.calculate_end_positions(self.player.get_positions()[piece_id], card)

        selection_made = False
        while not selection_made:
            # Title
            self.draw_box(720, 75, 280, 280, constants.BACKGROUND, constants.BACKGROUND)
            movement_group.empty()
            movement_group.add(Images(730, 75, 'images/movement/you_selected.png'))
            movement_group.add(Images(780, 110, 'images/movement/piece.png'))

            # Draw piece number
            if piece_id == 0:
                movement_group.add(Images(875, 119, 'images/movement/one.png'))
            elif piece_id == 1:
                movement_group.add(Images(875, 119, 'images/movement/two.png'))
            elif piece_id == 2:
                movement_group.add(Images(875, 119, 'images/movement/three.png'))
            else:
                movement_group.add(Images(875, 119, 'images/movement/four.png'))

            choices = []

            if 'start' in possible_moves:
                start = Images(770, 200 + (len(choices) * 60), 'images/movement/move_start_btn.png')
                movement_group.add(start)
                choices.append((start.get_rect(), 'start'))
            elif 'forward' in possible_moves:
                forward = Images(770, 200 + (len(choices) * 60), 'images/movement/forward_btn.png')
                movement_group.add(forward)
                choices.append((forward.get_rect(), 'forward'))

            elif 'backward' in possible_moves:
                backward = Images(770, 200 + (len(choices) * 60), 'images/movement/backward_btn.png')
                movement_group.add(backward)
                choices.append((backward.get_rect(), 'backward'))

            elif 'swap' in possible_moves:
                swap = Images(770, 200 + (len(choices) * 60), 'images/movement/swap_btn.png')
                movement_group.add(swap)
                choices.append((swap.get_rect(), 'swap'))

            cancel = Images(770, 200 + (len(choices) * 60), 'images/movement/cancel.png')
            movement_group.add(cancel)
            choices.append((cancel.get_rect(), 'cancel'))
            movement_group.draw(self.window)

            # Check for clicks
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    for rct, name in choices:
                        if rct.collidepoint(pos):
                            # If they canceled the move, allow them to reselect a piece and go through the process again
                            if name == 'cancel':
                                return self.handle_movement(card)

                            # Otherwise, update their end location based on what they selected
                            else:
                                if name in possible_moves:
                                    self.player.update_position(piece_id, possible_moves[name])
                                    selection_made = True

            pygame.display.update()

        # Update movement on server side
        self.get_server_response(f'update_position {self.player.get_positions()}')
        self.draw_screen()

        # Check if this is the start of a slide
        time.sleep(.25)
        self.player.update_position(piece_id, self.check_slide(self.player.get_positions()[piece_id]))
        self.get_server_response(f'update_position {self.player.get_positions()}')
        self.draw_screen()

        if val == Value.Two:
            # Draw again for two
            self.handle_turn()

        self.get_server_response('end_turn')

    def select_piece(self) -> int:
        """
        Listens for a mouse down click on a board square that contains one of the players pieces
        :return: Integer, the index of the piece the player clicked
        """

        selection = False
        while not selection:

            # Listen for a mouse click
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                    # Check if the click was on a square containing a piece
                    for ind, space_id in enumerate(self.player.get_positions()):
                        row = space_id // 16
                        col = space_id % 16

                        if col * constants.BOARD_SQUARE <= x <= (col + 1) * constants.BOARD_SQUARE and \
                           row * constants.BOARD_SQUARE <= y <= (row + 1) * constants.BOARD_SQUARE:
                            return ind

    def calculate_end_positions(self, start_pos, card) -> {str: int}:
        possible_moves = {}
        val = card.get_value()

        # One or Two
        if val == Value.One or val == Value.Two:
            if start_pos == self.player.get_start():
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
            # TODO: Add split option in later
            end_pos = self.calculate_forward_position(start_pos, 7)
            if not end_pos == -1:
                possible_moves['forward'] = end_pos

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

            end_pos = self.calculate_swap_position()
            if not end_pos == -1:
                possible_moves['swap'] = end_pos

        # Twelve:
        elif val == Value.Twelve:
            end_pos = self.calculate_forward_position(start_pos, 12)
            if not end_pos == -1:
                possible_moves['forward'] = end_pos

        # Sorry
        elif val == Value.Sorry:
            if start_pos == self.player.get_start():
                end_pos = self.calculate_swap_position()
                if not end_pos == -1:
                    possible_moves['swap'] = end_pos

        return possible_moves

    def calculate_forward_position(self, start_pos, moves) -> int:
        space_type = self.board.board[start_pos].get_type()

        # If this piece is not one that can be moved forward
        if space_type == ReservedType.START or space_type == ReservedType.HOME:
            return -1

        # Otherwise check that it can be moved the amount of spaces. If it reaches Home before then, it can't.
        space_ind = self.board.inorder_mapping.index(start_pos)

        while moves > 0:
            space_ind = (space_ind + 1) % len(self.board.inorder_mapping)
            space_type = self.board.board[self.board.inorder_mapping[space_ind]].get_type()

            if self.board.inorder_mapping[space_ind] == self.player.get_home():
                if moves != 1:
                    return -1
                moves -= 1

            # If this isn't a start/home or other colors safety then decrease the moves
            elif space_type != ReservedType.HOME and space_type != ReservedType.START and \
                    self.check_other_safety(self.board.inorder_mapping[space_ind]):
                moves -= 1

        return self.board.inorder_mapping[space_ind]

    def check_other_safety(self, space_id):
        space_type = self.board.board[space_id].get_type()
        color = self.player.get_color()

        if (color == 'Green' and space_type == ReservedType.GREEN_SAFETY) or \
           (color == 'Red' and space_type == ReservedType.RED_SAFETY) or \
           (color == 'Blue' and space_type == ReservedType.BLUE_SAFETY) or \
           (color == 'Yellow' and space_type == ReservedType.YELLOW_SAFETY):
            return True

        elif 'Safety' not in space_type.value:
            return True

        return False

    def check_slide(self, start_pos):
        space_value = self.board.board[start_pos].get_type().value
        if 'Slide' not in space_value:
            return start_pos

        # Can't take your own slide
        elif self.player.get_color() in space_value:
            return start_pos

        else:
            # Calculate the end position
            for key in constants.SLIDES.keys():
                for slide in constants.SLIDES[key]:

                    s, e = slide
                    if s == start_pos:
                        return e

        return start_pos

    def calculate_backward_position(self, start_pos, moves) -> int:
        return -1

    def calculate_swap_position(self) -> int:
        return -1
