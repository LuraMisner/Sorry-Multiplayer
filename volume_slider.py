import pygame
from images import Images


class VolumeSlider:
    def __init__(self, window, x_pos, y_pos, length, start_percentage, music_file,
                 marker_length=4, background_color=(0, 0, 0)):
        """
        Creates a volume slider
        :param window: Pygame surface
        :param x_pos: Integer, left x coord
        :param y_pos: Integer, y coord
        :param length: Integer, length
        :param start_percentage: Float, percentage as a decimal
        :param music_file: String, file path for audio
        :param marker_length: Integer, length of the mark representing the slider
        :param background_color: (Int, Int, Int), RGB value of background
        """
        self.window = window
        self.x = x_pos
        self.y = y_pos
        self.length = length
        self.marker_length = marker_length

        # Volume image
        self.image_group = pygame.sprite.Group()
        self.image_group.add(Images(self.x - 30, self.y - 12, 'images/volume.png'))

        # Start the volume at 50%
        self.current_position = x_pos + (length * min(start_percentage, 1))
        self.background_color = background_color
        self.draw_slider()

        # Background music
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)
        self.update_sound()

    def draw_slider(self):
        """
        Draws the visual for the volume bar and updates the window
        :return: None
        """
        self.draw_box(self.x - 30, self.y - self.marker_length, self.length + 35, (self.marker_length * 2) + 1,
                      0, self.background_color, self.background_color)

        pygame.draw.line(self.window, (0, 0, 0), (self.x, self.y), (self.x + self.length, self.y), 4)
        pygame.draw.line(self.window, (0, 0, 0), (self.current_position, self.y - (self.marker_length // 2)),
                         (self.current_position, self.y + (self.marker_length // 2)), 4)

        self.image_group.draw(self.window)
        pygame.display.flip()

    def draw_slider_start(self):
        """
        Draws the visual for the volume bar and updates the window
        :return: None
        """
        self.draw_box(self.x - 30, self.y - self.marker_length, self.length + 35, (self.marker_length * 2) + 1,
                      2, self.background_color, (0, 0, 0))

        pygame.draw.line(self.window, (0, 0, 0), (self.x, self.y), (self.x + self.length, self.y), 4)
        pygame.draw.line(self.window, (0, 0, 0), (self.current_position, self.y - (self.marker_length // 2)),
                         (self.current_position, self.y + (self.marker_length // 2)), 4)

        self.image_group.draw(self.window)

    def check_slider(self, x_click, y_click):
        """
        Checks if the user clicked around the volume bar
        :param x_click: Integer, x coord of mouse click
        :param y_click: Integer, y coord of mouse click
        :return: None
        """
        if y_click - 6 <= self.y <= y_click + 6 and self.x <= x_click <= self.x + self.length:
            self.update_slider()

    def update_slider(self):
        """
        Gets an end position for the current volume level and calls functions to update the visual and audio components
        :return: None
        """
        seen = False
        while not seen:
            # Update the cursor position to give a slide effect
            x, y = pygame.mouse.get_pos()
            self.current_position = max(self.x, min(self.x + self.length, x))
            self.draw_slider()
            self.update_sound()

            for event in pygame.event.get():
                # Wait for user to release the button
                if event.type == pygame.MOUSEBUTTONUP:
                    seen = True

    def update_sound(self):
        """
        Updates the audio component
        :return: None
        """
        # The sound is loud, so I'm scaling it to only go 30% of the maximum volume
        pygame.mixer.music.set_volume(((self.current_position - self.x) / self.length) * .3)

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

    def change_position(self, x, y):
        """
        Update the position of the bar
        :param x: Integer, new x coord
        :param y: Integer, new y coord
        :return: None
        """
        self.x = x
        self.y = y

        for img in self.image_group:
            img.update_position(self.x - 30, self.y - 12)

        self.draw_slider()

    def play_sound(self, sound_file):
        """
        Play a sound other than the main audio
        :param sound_file: String, path of file
        :return: None
        """
        self.pause_sound()
        sound = pygame.mixer.Sound.play(pygame.mixer.Sound(sound_file))
        sound.set_volume(((self.current_position - self.x) / self.length))
        self.unpause_sound()

    @staticmethod
    def pause_sound():
        """
        Pauses the main sound
        :return: None
        """
        pygame.mixer.pause()

    @staticmethod
    def unpause_sound():
        """
        Unpauses the main sound
        :return: None
        """
        pygame.mixer.unpause()
