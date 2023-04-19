from board import Board
import constants
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
        self.initialize_image_groups()

    def initialize_image_groups(self):
        title = Images(350, 175, 'images/start_screen/sorry_title.png')
        self.char_select_group.add(title)

        selection = Images(225, 330, 'images/start_screen/selected.png')
        self.char_select_group.add(selection)

        green = Images(140, 5, 'images/start_screen/green.png')
        self.char_select_group.add(green)

        red = Images(650, 5, 'images/start_screen/red.png')
        self.char_select_group.add(red)

        yellow = Images(140, 670, 'images/start_screen/yellow.png')
        self.char_select_group.add(yellow)

        blue = Images(650, 670, 'images/start_screen/blue.png')
        self.char_select_group.add(blue)

        confirm = Images(400, 400, 'images/start_screen/confirm.png')
        self.char_select_group.add(confirm)

    def get_server_response(self, query):
        return self.network.send(query)

    def select_color(self):
        selected = False
        choice = None
        select_group = pygame.sprite.Group()

        while not selected:
            # Draw out the colors
            self.draw_box(0, 0, constants.SELECT_X, constants.SELECT_Y, constants.GREEN, constants.BLACK)
            self.draw_box(500, 0, constants.SELECT_X, constants.SELECT_Y, constants.RED, constants.BLACK)
            self.draw_box(0, 375, constants.SELECT_X, constants.SELECT_Y, constants.YELLOW, constants.BLACK)
            self.draw_box(500, 375, constants.SELECT_X, constants.SELECT_Y, constants.BLUE, constants.BLACK)

            # If a color is no longer available, then grey it out
            available_colors = self.get_server_response('available_colors')
            if 'Green' not in available_colors:
                self.draw_transparent_box(0, 0, constants.SELECT_X, constants.SELECT_Y)
            if 'Red' not in available_colors:
                self.draw_transparent_box(500, 0, constants.SELECT_X, constants.SELECT_Y)
            if 'Yellow' not in available_colors:
                self.draw_transparent_box(0, 375, constants.SELECT_X, constants.SELECT_Y)
            if 'Blue' not in available_colors:
                self.draw_transparent_box(500, 375, constants.SELECT_X, constants.SELECT_Y)

            # Display the number ready
            rdy = self.get_server_response('num_ready')
            self.draw_text(f'{rdy[1]} / {rdy[0]} players ready', 24, constants.WHITE, 425, 450)

            # Look for a selection
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                    if 400 <= x <= 400 + constants.CONFIRM_X and 400 <= y <= 400 + constants.CONFIRM_Y:
                        if choice:
                            selected = True
                    elif 0 <= x <= constants.SELECT_X and 0 <= y <= constants.SELECT_Y:
                        choice = 'Green'
                        select_group.empty()
                        select_group.add(Images(500, 326, 'images/start_screen/green_small.png'))
                    elif 500 <= x <= 500 + constants.SELECT_X and 0 <= y <= constants.SELECT_Y:
                        choice = 'Red'
                        select_group.empty()
                        select_group.add(Images(490, 325, 'images/start_screen/red_small.png'))
                    elif 0 <= x <= constants.SELECT_X and 375 <= y <= 375 + constants.SELECT_Y:
                        choice = 'Yellow'
                        select_group.empty()
                        select_group.add(Images(505, 325, 'images/start_screen/yellow_small.png'))
                    elif 500 <= x <= 500 + constants.SELECT_X and 375 <= y <= 375 + constants.SELECT_Y:
                        choice = 'Blue'
                        select_group.empty()
                        select_group.add(Images(500, 325, 'images/start_screen/blue_small.png'))

            # Wait for a selection
            self.char_select_group.draw(self.window)
            select_group.draw(self.window)
            pygame.display.update()

        # Verify the selection with the server, if not verified recall the function
        verified = self.get_server_response(f'verify_choice {choice}')
        if not verified:
            return self.select_color()
        else:
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
