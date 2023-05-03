import constants
from player import Player
from deck import Deck


class Game:
    def __init__(self):
        self.player_count = 0
        self.players = []

        self.whos_turn = None
        self.deck = Deck()
        self.card = None

        self.available_colors = ['Red', 'Yellow', 'Green', 'Blue']

        self.positions = {}
        self.won = False
        self.winner = None

    def add_player(self, color):
        if color in self.available_colors:
            self.available_colors.remove(color)
            self.player_count += 1
            self.players.append(Player(color))
            return True

        return False

    def refresh_positions(self):
        self.positions = {}
        for player in self.players:
            self.positions[player.get_color()] = player.get_positions()

    def get_player_positions(self):
        self.refresh_positions()
        return self.positions

    def remove_player(self, color):
        for ind, p in enumerate(self.players):
            if p.get_color() == color:
                self.players.remove(p)
                self.player_count -= 1

                # If it is their turn make it the next persons turn
                if self.whos_turn == color:
                    self.whos_turn = self.players[(ind % len(self.players))].get_color()

    def get_turn(self):
        if not self.whos_turn:
            if self.player_count >= 1:
                self.whos_turn = self.players[0].get_color()
        return self.whos_turn

    def next_player(self):
        flag = False
        for ind, p in enumerate(self.players):
            if p.get_color() == self.whos_turn and not flag:
                self.whos_turn = self.players[(ind+1) % self.player_count].get_color()
                flag = True

    def current_card(self):
        if self.card:
            return self.card

    def draw_card(self):
        self.card = self.deck.draw_card()

    def get_player(self, color):
        if color:
            for p in self.players:
                if p.get_color() == color:
                    return p

    def update_player_location(self, color, positions):
        for p in self.players:
            if p.get_color() == color:
                p.update_positions(positions)

    def update_all_locations(self, player_pos):
        for key in player_pos.keys():
            self.update_player_location(key, player_pos[key])

    def check_win(self):
        self.refresh_positions()
        for p in self.players:
            color = p.get_color()
            if [constants.HOMES[color]] * 4 == self.positions[color]:
                self.won = True
                self.winner = color
