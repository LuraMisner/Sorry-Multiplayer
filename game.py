from player import Player


class Game:
    def __init__(self):
        self.player_count = 0
        self.players = []

        self.available_colors = ['Red', 'Yellow', 'Green', 'Blue']

        self.positions = {}
        self.won = False

    def add_player(self, color):
        if color in self.available_colors:
            self.available_colors.remove(color)
            self.player_count += 1
            self.players.append(Player(color))
            return True

        return False


