from board import Board
import constants
from card_value import Value
from images import Images
from network import Network
import pygame
from reserved_type import ReservedType
import sys
import time
from volume_slider import VolumeSlider


# noinspection PyTypeChecker
class Client:
    def __init__(self, win):
        self.window = win
        self.board = Board(self.window)
        self.network = Network()
        self.clock = pygame.time.Clock()

        self.color = None
        self.player_positions = {}
        self.pieces = []

        # Images
        self.char_select_group = pygame.sprite.Group()
        self.your_turn = pygame.sprite.Group()
        self.initialize_image_groups()

        # Background music
        self.mixer = VolumeSlider(self.window, 350, 270, 100, .25, 'sounds/background.mp3', 10, constants.BACKGROUND)

    def initialize_image_groups(self):
        """
        Initializes sprite groups and adds images to them
        """
        # Start screen
        self.char_select_group.add(Images(223, -50, 'images/start_screen/sorry_title.png'))
        self.char_select_group.add(Images(25, 90, 'images/start_screen/select_a_color.png'))
        self.char_select_group.add(Images(285, 285, 'images/start_screen/pawn2.png'))

        # Start screen menu
        self.char_select_group.add(Images(275, 490, 'images/start_screen/menu_background.png'))
        self.char_select_group.add(Images(285, 530, 'images/start_screen/confirm_grey.png'))
        self.char_select_group.add(Images(285, 590, 'images/start_screen/add_bot.png'))
        self.char_select_group.add(Images(285, 650, 'images/start_screen/remove_bot.png'))

        # Turn specific
        self.your_turn.add(Images(25, 205, 'images/titles/your_turn.png'))

    def get_server_response(self, query):
        """
        Sends a request to the server and gets a response
        :param query: String request being sent to the server
        :return: Reply from server. Could be nothing, or anything.
        """
        return self.network.send(query)

    def update_positions(self):
        """
        Updates all player positions
        """
        time.sleep(.1)
        self.player_positions = self.get_server_response('get_player_positions')

    def draw_start(self, color):
        """
        Draws out the start screen
        :param color: String representing color selected
        """

        # Outline the window
        pygame.draw.line(self.window, constants.BLACK, (0, 0), (0, 770), 6)
        pygame.draw.line(self.window, constants.BLACK, (0, 0), (770, 0), 6)
        pygame.draw.line(self.window, constants.BLACK, (770, 0), (770, 770), 6)
        pygame.draw.line(self.window, constants.BLACK, (0, 770), (770, 770), 6)

        # Green
        rect = pygame.Rect(6, 6, constants.SELECT_X - 6, constants.SELECT_Y - 6)
        pygame.draw.rect(self.window, constants.GREEN, rect)

        # Red
        rect = (constants.SELECT_X, 6, constants.SELECT_X - 6, constants.SELECT_Y - 6)
        pygame.draw.rect(self.window, constants.RED, rect)

        # Yellow
        rect = pygame.Rect(6, constants.SELECT_Y, constants.SELECT_X - 6, constants.SELECT_Y - 6)
        pygame.draw.rect(self.window, constants.YELLOW, rect)

        # Blue
        rect = (constants.SELECT_X, constants.SELECT_Y, constants.SELECT_X - 6, constants.SELECT_Y - 6)
        pygame.draw.rect(self.window, constants.BLUE, rect)

        selected = pygame.sprite.Group()

        # If a color is no longer available, then grey it out
        available_colors = self.get_server_response('available_colors')
        if 'Green' not in available_colors:
            self.draw_transparent_box(0, 0, constants.SELECT_X, constants.SELECT_Y, 180)
        else:
            selected.add(Images(143, 143, 'images/start_screen/click.png'))

        if 'Red' not in available_colors:
            self.draw_transparent_box(constants.SELECT_X, 0, constants.SELECT_X, constants.SELECT_Y, 180)
        else:
            selected.add(Images(527, 143, 'images/start_screen/click.png'))

        if 'Yellow' not in available_colors:
            self.draw_transparent_box(0, constants.SELECT_Y, constants.SELECT_X, constants.SELECT_Y, 180)
        else:
            selected.add(Images(143, 527, 'images/start_screen/click.png'))

        if 'Blue' not in available_colors:
            self.draw_transparent_box(constants.SELECT_X, constants.SELECT_Y,
                                      constants.SELECT_X, constants.SELECT_Y, 180)
        else:
            selected.add(Images(527, 527, 'images/start_screen/click.png'))

        # Visual for the color selected
        if color == 'Green':
            self.draw_box(285, 285, 200, 200, 2, constants.GREEN, constants.BLACK)
            selected.add(Images(285, 288, 'images/start_screen/green_xs.png'))
        elif color == 'Blue':
            self.draw_box(285, 285, 200, 200, 2, constants.BLUE, constants.BLACK)
            selected.add(Images(285, 288, 'images/start_screen/blue_xs.png'))
        elif color == 'Red':
            self.draw_box(285, 285, 200, 200, 2, constants.RED, constants.BLACK)
            selected.add(Images(285, 288, 'images/start_screen/red_xs.png'))
        elif color == 'Yellow':
            self.draw_box(285, 285, 200, 200, 2, constants.YELLOW, constants.BLACK)
            selected.add(Images(285, 288, 'images/start_screen/yellow_xs.png'))
        else:
            self.draw_box(285, 285, 200, 200, 2, constants.WHITE, constants.BLACK)

        self.char_select_group.draw(self.window)
        selected.draw(self.window)

    def select_color(self):
        """
        Draws the character select screen and lets the player select a color to be. Updates it on the server side
        """
        selected = False
        choice = None
        conf_group = pygame.sprite.Group()
        conf_group.add(Images(285, 530, 'images/start_screen/confirm.png'))

        while not selected:
            self.draw_start(choice)
            self.mixer.draw_slider_start()

            # Display the number ready
            rdy = self.get_server_response('num_ready')
            self.draw_text(f'{rdy[1]} / {rdy[0]} players ready', 24, constants.WHITE, 315, 500)

            # Look for a selection
            event = pygame.event.get()
            for ev in event:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.mixer.check_slider(x, y)

                if ev.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                    if 285 <= x <= 285 + constants.CONFIRM_X and 530 <= y <= 530 + constants.CONFIRM_Y:
                        if choice:
                            selected = True
                    elif 0 <= x <= constants.SELECT_X and 0 <= y <= constants.SELECT_Y:
                        choice = 'Green'
                    elif 385 <= x <= 385 + constants.SELECT_X and 0 <= y <= constants.SELECT_Y:
                        choice = 'Red'
                    elif 0 <= x <= constants.SELECT_X and 385 <= y <= 385 + constants.SELECT_Y:
                        choice = 'Yellow'
                    elif 385 <= x <= 385 + constants.SELECT_X and 385 <= y <= 385 + constants.SELECT_Y:
                        choice = 'Blue'

                    # Check if they are adding or removing a bot, send request to server
                    if 285 <= x <= 485 and 590 <= y <= 630:
                        self.get_server_response('add_bot')
                    elif 285 <= x <= 485 and 650 <= y <= 690:
                        self.get_server_response('remove_bot')

                if ev.type == pygame.QUIT:
                    self.get_server_response('quit')
                    sys.exit()

            # Wait for a selection
            if choice:
                for img in self.char_select_group:
                    if img.get_path() == 'images/start_screen/confirm_grey.png':
                        img.change_path('images/start_screen/confirm.png')

            pygame.display.update()
            self.clock.tick(60)

        # Verify the selection with the server, if not verified recall the function
        verified = self.get_server_response(f'verify_choice {choice}')
        if not verified:
            return self.select_color()
        else:
            self.color = choice
            return self.wait_for_start()

    def wait_for_start(self):
        """
        Function for updating the screen waiting for all players to be ready (after this player is ready)
        """
        start = self.get_server_response('start')
        while not start:
            rdy = self.get_server_response('num_ready')
            self.draw_start(self.color)
            self.mixer.draw_slider_start()

            self.draw_text(f'{rdy[1]} / {rdy[0]} players ready', 24, constants.WHITE, 315, 500)

            event = pygame.event.get()
            for ev in event:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    # Check if the click was on the volume slider
                    self.mixer.check_slider(x, y)

                    # Check if they are adding or removing a bot, send request to server
                    if 285 <= x <= 485 and 590 <= y <= 630:
                        self.get_server_response('add_bot')
                    elif 285 <= x <= 485 and 650 <= y <= 690:
                        self.get_server_response('remove_bot')

                if ev.type == pygame.QUIT:
                    self.get_server_response('quit')
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)

            start = self.get_server_response('start')

        self.update_positions()
        self.mixer.change_position(350, 210)

    def draw_box(self, x, y, x_length, y_length, outline_width, color, outline):
        """
        Draws a box on the window
        :param x: Integer, x position of top left corner
        :param y: Integer, y position of top left corner
        :param x_length: Integer, length
        :param y_length: Integer, height
        :param outline_width: Integer, width of outline
        :param color: (int, int, int), color of box
        :param outline: (int, int, int), color of outline
        """

        background = pygame.Rect(x, y, x_length, y_length)
        pygame.draw.rect(self.window, outline, background)
        rect = pygame.Rect(x + outline_width, y + outline_width,
                           x_length - (2 * outline_width), y_length - (2 * outline_width))
        pygame.draw.rect(self.window, color, rect)

    def draw_transparent_box(self, x, y, width, height, al):
        """
        Draws a transparent box, used to highlight locations
        :param x: Integer top-left x position
        :param y: Integer top-left y position
        :param width: Integer
        :param height: Integer
        :param al: Integer to determine the alpha number
        """
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        s.fill((0, 0, 0, al))
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
        """
        Draws all player pieces on the board
        """
        self.update_positions()
        self.pieces = []
        pieces_group = pygame.sprite.Group()

        for player in self.player_positions.keys():
            for ind, piece in enumerate(self.player_positions[player]):

                # Determine the location
                if self.player_positions[player][ind] == constants.STARTS[player]:
                    x, y = constants.START_DISPLAYS[player][ind]
                elif self.player_positions[player][ind] == constants.HOMES[player]:
                    x, y = constants.HOME_DISPLAYS[player][ind]
                else:
                    y = constants.BOARD_SQUARE * (piece // 16)
                    x = constants.BOARD_SQUARE * (piece % 16)

                # Adjust the x,y to center it
                x = x + 4
                y = y + 4

                # If the piece is in start, white outline.
                if self.player_positions[player][ind] == constants.STARTS[player] or \
                   self.player_positions[player][ind] == constants.HOMES[player]:
                    if player == 'Green':
                        circ = Images(x, y, 'images/pieces/green_w.png')
                    elif player == 'Red':
                        circ = Images(x, y, 'images/pieces/red_w.png')
                    elif player == 'Blue':
                        circ = Images(x, y, 'images/pieces/blue_w.png')
                    else:
                        circ = Images(x, y, 'images/pieces/yellow_w.png')

                # Otherwise, black outline
                else:
                    if player == 'Green':
                        circ = Images(x, y, 'images/pieces/green_b.png')
                    elif player == 'Red':
                        circ = Images(x, y, 'images/pieces/red_b.png')
                    elif player == 'Blue':
                        circ = Images(x, y, 'images/pieces/blue_b.png')
                    else:
                        circ = Images(x, y, 'images/pieces/yellow_b.png')

                if self.color == player:
                    self.pieces.append(circ.get_rect())

                pieces_group.add(circ)

        # Draw the pieces onto the window
        pieces_group.draw(self.window)

    def draw_screen(self):
        """
        Draws everything that needs to be on the board in each refresh
        """
        self.window.fill(constants.BACKGROUND)
        self.board.draw_board()
        self.draw_players()
        self.draw_card()
        self.mixer.draw_slider()

        # Turn indicator
        reply = self.get_server_response('whos_turn')
        if reply == 'Green':
            self.draw_box(315, 230, 150, 8, 0, constants.GREEN, constants.GREEN)
        elif reply == 'Red':
            self.draw_box(315, 230, 150, 8, 0, constants.RED, constants.RED)
        elif reply == 'Blue':
            self.draw_box(315, 230, 150, 8, 0, constants.BLUE, constants.BLUE)
        elif reply == 'Yellow':
            self.draw_box(315, 230, 150, 8, 0, constants.YELLOW, constants.YELLOW)

        pygame.display.update()

    def draw_card(self):
        """
        Draws the card representing the card drawn
        """
        card_group = pygame.sprite.Group()
        card = self.get_server_response('get_card')
        if card:
            val = card.get_value()

            if val == Value.One:
                card_group.add(Images(315, 245, 'images/cards/one.png'))
            elif val == Value.Two:
                card_group.add(Images(315, 245, 'images/cards/two.png'))
            elif val == Value.Three:
                card_group.add(Images(315, 245, 'images/cards/three.png'))
            elif val == Value.Four:
                card_group.add(Images(315, 245, 'images/cards/four.png'))
            elif val == Value.Five:
                card_group.add(Images(315, 245, 'images/cards/five.png'))
            elif val == Value.Seven:
                card_group.add(Images(315, 245, 'images/cards/seven.png'))
            elif val == Value.Eight:
                card_group.add(Images(315, 245, 'images/cards/eight.png'))
            elif val == Value.Ten:
                card_group.add(Images(315, 245, 'images/cards/ten.png'))
            elif val == Value.Eleven:
                card_group.add(Images(315, 245, 'images/cards/eleven.png'))
            elif val == Value.Twelve:
                card_group.add(Images(315, 245, 'images/cards/twelve.png'))
            else:
                card_group.add(Images(315, 245, 'images/cards/sorry.png'))

            card_group.draw(self.window)

    def check_our_turn(self):
        """
        Checks the server to see if it is the players turn, if so it calls a function to handle the turn
        """
        reply = self.get_server_response('whos_turn')
        if reply == self.color:
            self.handle_turn()

    def handle_turn(self):
        """
        Updates player positions, draws the card for the players turn and then sends them to handle the movement
        """
        self.update_positions()

        # Let the user draw a card
        self.your_turn.draw(self.window)
        pygame.display.flip()
        time.sleep(1.75)

        # Draw a card button
        draw_btn = pygame.sprite.Group()
        draw = Images(315, 500, 'images/titles/draw.png')
        draw_btn.add(Images(315, 535, 'images/titles/draw_btn_space.png'))
        draw_btn.add(draw)

        self.draw_screen()
        draw_btn.draw(self.window)
        pygame.display.flip()

        card_drawn = False
        while not card_drawn:

            event = pygame.event.get()
            for ev in event:
                if ev.type == pygame.MOUSEBUTTONDOWN and not card_drawn:
                    self.check_slider()

                    pos = pygame.mouse.get_pos()
                    if draw.rect.collidepoint(pos):
                        self.get_server_response('draw_card')
                        self.mixer.play_sound('sounds/card-flip.mp3')
                        card_drawn = True

                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE and not card_drawn:
                    self.get_server_response('draw_card')
                    card_drawn = True

                if ev.type == pygame.QUIT:
                    self.get_server_response('quit')
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)

        self.handle_movement(self.get_server_response('get_card'))

    def handle_movement(self, card):
        """
        Handles the user selection a piece and a move to make, and updates it server side
        :param card: Card object of the card drawn
        """
        # Refresh the screen
        self.draw_screen()

        possible_moves = self.check_possible(self.player_positions[self.color], card)
        if possible_moves == {0: {}, 1: {}, 2: {}, 3: {}} or not self.check_moves(possible_moves):
            # Do something here to show there is no moves
            self.no_possible_moves()
            self.get_server_response('end_turn')
            return

        # Calculate valid moves
        val = card.get_value()
        self.draw_click_icon(possible_moves)
        piece_id = self.select_piece(possible_moves)

        # Let the user select from the possible choices
        if 'split' in possible_moves[piece_id]:
            # Only need to call the split function, because they can move it 7 spaces or split it.
            new_positions = self.handle_split(piece_id)

            if new_positions == [-1]:
                return self.handle_movement(card)

            self.player_positions[self.color] = new_positions
        else:
            end_pos = set()
            for key in possible_moves[piece_id].keys():
                if possible_moves[piece_id][key] != -1:
                    end_pos.add(possible_moves[piece_id][key])

            if 'swap' in possible_moves[piece_id]:
                end_pos.update(self.calculate_swap_position())

            # Highlights the possible positions and allows the user to select one
            end = self.select_end_position(end_pos)
            if end == -1:
                return self.handle_movement(card)

            if val == Value.Eleven:
                if end in self.calculate_swap_position():
                    # Handles the swap for eleven card if a swap was chosen. If a player is exactly 11 spaces
                    # ahead, it prioritizes sending the player home rather than swapping.
                    if 'forward' not in possible_moves[piece_id] or \
                       possible_moves[piece_id]['forward'] != end:

                        # Eleven card, swap places with the other piece
                        for k in self.player_positions.keys():
                            if k != self.color:
                                if end in self.player_positions[k]:
                                    ind = self.player_positions[k].index(end)
                                    self.player_positions[k][ind] = self.player_positions[self.color][piece_id]
                                    self.get_server_response(f'add_log {k},swapped')

                    self.get_server_response(f'update_all_positions {self.player_positions}')

            self.player_positions[self.color][piece_id] = end

        # Update movement on server side
        self.get_server_response(f'update_position {self.player_positions[self.color]}')
        self.draw_screen()
        self.check_occupied(self.player_positions[self.color][piece_id], piece_id)

        # Check if this is the start of a slide
        time.sleep(.2)
        self.player_positions[self.color][piece_id] = \
            self.check_slide(self.player_positions[self.color][piece_id], piece_id)
        self.get_server_response(f'update_position {self.player_positions[self.color]}')
        self.draw_screen()

        # Draw again if you drew a two (if you didn't win on that move)
        if val == Value.Two and not self.get_server_response('check_won'):
            return self.handle_turn()

        # End the turn
        self.get_server_response('end_turn')

    def check_moves(self, possible_moves) -> bool:
        """
        Checks if there is at least one move that can be made that isn't to a space occupied by your own piece
        :param possible_moves: Dictionary mapping pieces to end position
        :return: Boolean
        """
        for dic in possible_moves.keys():
            for key in possible_moves[dic].keys():
                if possible_moves[dic][key] == constants.HOMES[self.color] or \
                        possible_moves[dic][key] not in self.player_positions[self.color]:
                    return True

        return False

    def draw_click_icon(self, options):
        """
        Draws a select icon on the screen
        :param options: Dictionary of pieces and their mapped to their valid moves
        :return: None
        """
        click_group = pygame.sprite.Group()
        for ind, p in enumerate(self.pieces):
            if options[ind] != {}:
                # Draw a click icon
                x, y = p.x, p.y
                click_group.add(Images(x+4, y+4, 'images/titles/click_xs_2.png'))

        click_group.draw(self.window)
        click_group.draw(self.window)
        pygame.display.update()

    def select_piece(self, moves) -> int:
        """
        Listens for a mouse down click on a board square that contains one of the players pieces
        :param moves: Dictionary of moves each piece can make {int: {string: int}.
        :return: Integer, the index of the piece the player clicked
        """
        selection = False
        while not selection:

            # Listen for a mouse click
            event = pygame.event.get()
            for ev in event:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.check_slider()

                if ev.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    for i in range(len(self.pieces)):
                        if self.pieces[i].collidepoint(pos) and moves[i] != {}:
                            return i

                if ev.type == pygame.QUIT:
                    self.get_server_response('quit')
                    sys.exit()

            self.clock.tick(60)

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
                possible_moves['split'] = -1

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
                if len(end_pos) == 1:
                    possible_moves['swap'] = end_pos[0]
                elif len(end_pos) > 0:
                    possible_moves['swap'] = -1

        # Twelve:
        elif val == Value.Twelve:
            end_pos = self.calculate_forward_position(start_pos, 12)
            if not end_pos == -1:
                possible_moves['forward'] = end_pos

        # Sorry
        elif val == Value.Sorry:
            if start_pos == constants.STARTS[self.color]:
                end_pos = self.calculate_swap_position()

                if len(end_pos) == 1:
                    possible_moves['swap'] = end_pos[0]
                elif len(end_pos) > 0:
                    possible_moves['swap'] = -1

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

    def check_slide(self, start_pos, piece_id) -> int:
        """
        Checks if the end position is the start of a slide, and updates the position accordingly
        :param start_pos: Integer of start position
        :param piece_id: Integer representing the pieces index
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

                        # Slide sound effect
                        self.mixer.play_sound('sounds/slide.mp3')

                        for i in range(s_ind, e_ind + 1):
                            s_id = self.board.inorder_mapping[i]
                            if 'Slide' in self.board.board[s_id].get_type().value:
                                self.check_occupied(self.board.inorder_mapping[i], piece_id)

                        return e

        return start_pos

    def check_occupied(self, space_id, index):
        """
        Checks if a space is already occupied by another player, and handles the necessary adjustments to positions
        for sending them back to start.
        :param space_id: Integer of the space ID
        :param index: Index of the piece that is being moved there
        """
        self.update_positions()

        for key in self.player_positions.keys():
            if key != self.color:
                if space_id in self.player_positions[key]:
                    ind = self.player_positions[key].index(space_id)

                    # Need to move the player back to their spawn
                    self.get_server_response(f'add_log {key},bh')
                    self.player_positions[key][ind] = constants.STARTS[key]
            else:
                # Need to make sure you aren't counting the one that just moved, or any in the home
                for ind, space in enumerate(self.player_positions[self.color]):
                    if space == space_id and ind != index and space_id != constants.HOMES[self.color]:
                        self.player_positions[self.color][ind] = constants.STARTS[self.color]

        # Update it back on the server side
        self.get_server_response(f'update_all_positions {self.player_positions}')

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
        self.update_positions()

        # Find the end positions
        end_positions = []
        for key in self.player_positions.keys():
            if key != self.color:
                for item in self.player_positions[key]:
                    # If the player is not in a start, home, or safety zone then they may swap
                    space_type = self.board.board[item].get_type()
                    if space_type != ReservedType.HOME and space_type != ReservedType.START and \
                            'Safety' not in space_type.value:
                        end_positions.append(item)

        return end_positions

    def check_possible(self, positions, card) -> {int: {str: int}}:
        """
        Checks how many pieces there are movements for
        :param positions: Array of integers representing current piece locations
        :param card: Card object that was drawn
        :return: Boolean representing if there is at least one possible move
        """
        result = {}
        for ind, p in enumerate(positions):
            result[ind] = self.calculate_end_positions(p, card)

        return result

    def pick_swap(self) -> int:
        """
        Allows user to pick another users piece to swap positions with
        :return: Integer representing the id of the space selected
        """
        self.draw_screen()
        possible_swaps = self.calculate_swap_position()

        # Only one solution
        if len(possible_swaps) == 1:
            return possible_swaps[0]

        selected = None
        selection = False

        # Draw the end positions
        for position in possible_swaps:
            x = position // 16
            y = position % 16

            self.draw_transparent_box(y * constants.BOARD_SQUARE, x * constants.BOARD_SQUARE,
                                      constants.BOARD_SQUARE, constants.BOARD_SQUARE, 100)

        pygame.display.update()

        while not selection:
            events = pygame.event.get()
            for ev in events:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.check_slider()
                    x, y = pygame.mouse.get_pos()

                    space_id = ((y // constants.BOARD_SQUARE) * 16) + (x // constants.BOARD_SQUARE)
                    if space_id in possible_swaps:
                        selected = space_id
                        selection = True

                if ev.type == pygame.QUIT:
                    self.get_server_response('quit')
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)

        return selected

    def no_possible_moves(self):
        """
        Displays a notice that there is no possible moves for the user
        """
        self.draw_screen()
        title_group = pygame.sprite.Group()
        title_group.add(Images(25, 205, 'images/titles/no_moves.png'))
        title_group.draw(self.window)
        pygame.display.update()
        time.sleep(1.75)

    def check_forward(self) -> [int]:
        """
        Calculate how many moves forward the pieces can go for the 7 split
        :return: array of integers
        """
        results = []

        # Find the largest amount of steps each piece can take.
        for p in self.player_positions[self.color]:
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

        # If any two add up to 7 or more, then return True
        results.sort()

        if results[2] + results[3] >= 7:
            return True

        return False

    def draw_split_positions(self, ind, max_moves) -> int:
        """
        Highlights and lets the user select a position on the board for how many spaces they want to move
        :param ind: Piece index
        :param max_moves: Maximum number of moves they can make
        :return: Integer, how many spaces the piece moved
        """
        end_pos = []
        moves = []
        self.draw_screen()
        results = self.check_forward()

        # Highlight all possible end locations for the piece
        for i in range(1, max_moves+1):
            end_position = self.calculate_forward_position(self.player_positions[self.color][ind], i)

            # Make sure there is another piece that can be moved the remaining spaces
            flag = False
            for n in range(len(results)):
                if n != ind and results[n] >= (7-i):
                    flag = True

            if end_position != -1 and flag:
                end_pos.append(end_position)
                moves.append(i)

        selected = self.select_end_position(end_pos)
        if selected == -1:
            return -1

        index = end_pos.index(selected)
        return moves[index]

    def handle_split(self, ind) -> [int]:
        """
        Main function for selecting the pieces and moves being made from the 7 split
        :param ind: Index of the first selected piece
        :return: Array of Integers, representing the new positions of the pieces
        """
        positions = self.player_positions[self.color]
        max_moves = 7

        # Calculate the first end position
        first_move = self.draw_split_positions(ind, max_moves)
        if first_move == -1:
            return [-1]

        # Update the position
        positions[ind] = self.calculate_forward_position(positions[ind], first_move)
        self.check_occupied(positions[ind], ind)
        positions[ind] = self.check_slide(positions[ind], ind)

        # Draw updated position
        self.get_server_response(f'update_position {positions}')
        self.draw_screen()

        max_moves -= first_move
        if max_moves > 0:
            positions = self.handle_second_piece(max_moves)

        return positions

    def handle_second_piece(self, max_moves) -> [int]:
        """
        Handles the selection of the second piece in a seven split card
        :param max_moves: Integer, moves left
        :return: Array of Integers representing the positions of the pieces after the moves
        """
        positions = self.player_positions[self.color]

        # Visuals for who can be picked
        moves = {}
        for ind in range(4):
            end_pos = self.calculate_forward_position(positions[ind], max_moves)
            if end_pos == -1:
                moves[ind] = {}
            else:
                moves[ind] = {'forward': end_pos}

        # Visually update the screen
        self.draw_moves_left(max_moves)
        self.draw_screen()

        # Calculate the second end position
        self.draw_click_icon(moves)
        pygame.display.flip()

        # Show the end positions
        second_piece = self.select_piece(moves)
        end_pos = self.select_end_position([self.calculate_forward_position(positions[second_piece], max_moves)])

        # User switches piece
        if end_pos == -1:
            return self.handle_second_piece(max_moves)

        # Handle occupied or slides
        self.check_occupied(positions[second_piece], second_piece)
        positions[second_piece] = self.check_slide(end_pos, second_piece)

        return positions

    def draw_moves_left(self, moves):
        """
        Displays a message that lets the user know how many moves they have left
        :param moves: Integer, number of moves left
        """
        self.draw_screen()

        title = pygame.sprite.Group()
        if moves == 1:
            title.add(Images(25, 285, 'images/titles/split/1_space.png'))
        elif moves == 2:
            title.add(Images(25, 285, 'images/titles/split/2_spaces.png'))
        elif moves == 3:
            title.add(Images(25, 285, 'images/titles/split/3_spaces.png'))
        elif moves == 4:
            title.add(Images(25, 285, 'images/titles/split/4_spaces.png'))
        elif moves == 5:
            title.add(Images(25, 285, 'images/titles/split/5_spaces.png'))
        elif moves == 6:
            title.add(Images(25, 285, 'images/titles/split/6_spaces.png'))

        title.draw(self.window)
        pygame.display.update()
        time.sleep(1.6)

    def select_end_position(self, end_positions) -> int:
        """
        Allows user to select an end position from the list of positions
        :param end_positions: Array of integers
        :return: Integer
        """
        # Title telling user how to select an end position
        title = pygame.sprite.Group()
        title.add(Images(25, 285, 'images/titles/end_pos.png'))
        title.draw(self.window)
        pygame.display.flip()
        time.sleep(1.7)

        self.draw_screen()

        # Button to let user select a different piece
        new_piece = pygame.sprite.Group()
        new_piece_btn = Images(315, 500, 'images/titles/different_piece.png')
        new_piece.add(new_piece_btn)
        new_piece.draw(self.window)

        # Highlight the positions
        for i in end_positions:
            x = (i % 16) * constants.BOARD_SQUARE
            y = (i // 16) * constants.BOARD_SQUARE

            self.draw_transparent_box(x, y, constants.BOARD_SQUARE, constants.BOARD_SQUARE, 100)

        pygame.display.flip()

        # Wait for the selection
        while True:
            events = pygame.event.get()
            for ev in events:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.check_slider()

                    x, y = pygame.mouse.get_pos()
                    space_id = ((y // constants.BOARD_SQUARE) * 16) + (x // constants.BOARD_SQUARE)

                    if space_id in end_positions:
                        return space_id

                    elif new_piece_btn.rect.collidepoint(x, y):
                        return -1

                if ev.type == pygame.QUIT:
                    self.get_server_response('quit')
                    sys.exit()

            self.clock.tick(60)

    def check_log(self):
        """
        Checks if there is a message for the user, if so it displays an image to the user
        :return: None
        """
        reply = self.get_server_response('check_log')
        if reply:
            self.draw_screen()
            alert = pygame.sprite.Group()

            if reply == 'bh':
                alert.add(Images(25, 285, 'images/titles/sent_start.png'))
            elif reply == 'swapped':
                alert.add(Images(25, 285, 'images/titles/swapped_places.png'))

            # Display the message to the user
            alert.draw(self.window)
            pygame.display.update()
            time.sleep(2)

    def check_slider(self):
        """
        Checks if the volume slider was selected
        :return: None
        """
        x, y = pygame.mouse.get_pos()
        self.mixer.check_slider(x, y)

    def win_screen(self):
        """
        Draws the end screen once someone has won the game
        """
        winner = self.get_server_response('winner')

        title_group = pygame.sprite.Group()
        self.window.fill(constants.BACKGROUND)

        # Titles
        if self.color == winner:
            title_group.add(Images(10, 100, 'images/end_screen/congrats.png'))

            if winner == 'Red':
                title_group.add(Images(10, 250, 'images/end_screen/you_r.png'))
            elif winner == 'Blue':
                title_group.add(Images(10, 250, 'images/end_screen/you_b.png'))
            elif winner == 'Green':
                title_group.add(Images(10, 250, 'images/end_screen/you_g.png'))
            else:
                title_group.add(Images(10, 250, 'images/end_screen/you_y.png'))

        elif winner == 'Red':
            title_group.add(Images(10, 100, 'images/end_screen/red_wins.png'))
        elif winner == 'Blue':
            title_group.add(Images(10, 100, 'images/end_screen/blue_wins.png'))
        elif winner == 'Green':
            title_group.add(Images(10, 100, 'images/end_screen/green_wins.png'))
        else:
            title_group.add(Images(10, 100, 'images/end_screen/yellow_wins.png'))

        # Play again and Exit buttons
        title_group.add(Images(235, 500, 'images/titles/play_again.png'))
        title_group.add(Images(235, 600, 'images/titles/exit_btn.png'))

        num_ready = self.get_server_response('new_game_votes')
        self.draw_text(f'{num_ready[0]} / {num_ready[1]} players', 18, constants.BLACK, 350, 570)

        title_group.draw(self.window)

    def handle_win(self):
        """
        Draws the win screen and waits for the user to exit, or ready up to play again.
        """
        # Sound effects and images
        self.mixer.pause_sound()

        readied_group = pygame.sprite.Group()
        readied_group.add(Images(290, 450, 'images/titles/readied_up.png'))

        # This allows it to only play the effect once, because we wait for them to ready or exit
        if not self.get_server_response('check_vote'):
            self.mixer.play_sound('sounds/win.mp3')

        # Check for a button press
        while not self.get_server_response('check_vote') and self.get_server_response('check_won'):
            self.win_screen()
            pygame.display.update()
            self.clock.tick(60)

            # Check if they click play again or exit
            event = pygame.event.get()
            for ev in event:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    if 235 <= x <= 535 and 500 <= y <= 560:
                        # Play again
                        print('Readied up')
                        self.mixer.unpause_sound()
                        self.get_server_response('new_game')

                    if 235 <= x <= 535 and 600 <= y <= 660:
                        # Exit
                        self.get_server_response('quit')
                        sys.exit()

        self.get_server_response('start_new_game')

        # Adds the readied up message
        self.win_screen()
        readied_group.draw(self.window)
        pygame.display.update()

        # If they quit after readying up
        event = pygame.event.get()
        for ev in event:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if 235 <= x <= 535 and 600 <= y <= 660:
                    # Exit
                    self.get_server_response('quit')
                    sys.exit()
