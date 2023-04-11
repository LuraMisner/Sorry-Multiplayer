
class Player:
    def __init__(self, color, board):
        self.color = color
        self.board = board

        # slides has the start and end index for a slide
        if color == "Green":
            self.safety_start = 3
            self.home = 8
            self.start = 11
            self.slides = [[23, 32], [38, 42], [45, 54], [60, 64], [67, 76], [82, 86]]
        elif color == "Red":
            self.safety_start = 25
            self.home = 30
            self.start = 33
            self.slides = [[1, 10], [16, 20], [45, 54], [60, 64], [67, 76], [82, 86]]
        elif color == "Blue":
            self.safety_start = 47
            self.home = 52
            self.start = 55
            self.slides = [[1, 10], [16, 20], [23, 32], [38, 42], [67, 76], [82, 86]]
        else:
            # yellow
            self.safety_start = 69
            self.home = 74
            self.start = 77
            self.slides = [[1, 10], [16, 20], [23, 32], [38, 42], [45, 54], [60, 64]]

    def get_color(self):
        return self.color

    def get_board(self):
        return self.board

    def set_color(self, color):
        self.color = color

    def set_board(self, board):
        self.board = board