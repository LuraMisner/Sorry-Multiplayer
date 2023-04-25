from board import Board
import constants
from card_value import Value
from images import Images
from network import Network
import pygame


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

        val = card.get_value()
        piece_id = self.select_piece()
        piece_location = self.player.get_positions()[piece_id]

        # TODO: Figure out why these images get blurry
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

        self.draw_screen()
        movement_group.draw(self.window)
        pygame.display.flip()

        selection_made = False
        while not selection_made:
            self.draw_box(720, 75, 280, 280, constants.BACKGROUND, constants.BACKGROUND)
            choices = []

            # Calculate the options and let them select one
            if val == Value.One or val == Value.Two:
                # Either move forward or move a piece out from the start
                if piece_location == self.player.get_start():
                    start = Images(770, 200 + (len(choices) * 60), 'images/movement/move_start_btn.png')
                    movement_group.add(start)
                    choices.append((start.get_rect(), 'start'))
                else:
                    forward = Images(770, 200 + (len(choices) * 60), 'images/movement/forward_btn.png')
                    movement_group.add(forward)
                    choices.append((forward.get_rect(), 'forward'))

                cancel = Images(770, 200 + (len(choices) * 60), 'images/movement/cancel.png')
                movement_group.add(cancel)
                choices.append((cancel.get_rect(), 'cancel'))

                movement_group.draw(self.window)

            elif val == Value.Three or val == Value.Five or val == Value.Eight or val == Value.Twelve:
                # Can only move forward
                selection_made = True

            elif val == Value.Four:
                # Move backwards
                selection_made = True

            elif val == Value.Seven:
                # Can move forward 7 or split between 2 pieces
                selection_made = True

            elif val == Value.Ten:
                # Move forward 10 or backwards 1
                selection_made = True

            elif val == Value.Eleven:
                # Move forward 11 or swap places with another player
                selection_made = True

            elif val == Value.Sorry:
                # Move a piece from spawn to swap with a player (can be any piece if none in spawn)
                selection_made = True

            # Check for clicks
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    for rct, name in choices:
                        if rct.collidepoint(pos):
                            if name == 'cancel':
                                return self.handle_movement(card)
                            else:
                                pass
                            selection_made = True

            pygame.display.update()

        # TODO: Update movement on server side

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
