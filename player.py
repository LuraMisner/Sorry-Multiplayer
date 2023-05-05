import constants


class Player:
    def __init__(self, color):
        self.color = color
        self.safety_start = constants.SAFETY_STARTS[self.color]
        self.home = constants.HOMES[self.color]
        self.start = constants.STARTS[self.color]
        self.slides = constants.SLIDES[self.color]
        self.positions = [constants.STARTS[self.color]] * 4

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
