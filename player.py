import constants


class Player:
    def __init__(self, color):
        self.color = color

        self.safety_start = constants.SAFETY_STARTS[self.color]
        self.home = constants.HOMES[self.color]
        self.start = constants.STARTS[self.color]
        self.slides = constants.SLIDES[self.color]

    def get_color(self):
        return self.color
