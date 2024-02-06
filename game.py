import constants
import copy
from bot import Bot
from card import Card
from card_value import Value
from deck import Deck
from player import Player


class Game:
    def __init__(self):
        self.players = []
        self.logs = {'Red': [], 'Yellow': [], 'Green': [], 'Blue': []}

        self.whos_turn = None
        self.deck = Deck()
        self.card = None

        self.available_colors = ['Red', 'Yellow', 'Green', 'Blue']
        self.sorted = False

        self.positions = {}
        self.won = False
        self.winner = None

    def order_players(self):
        """
        Puts the list of players in order from the first person going clockwise
        """
        if not self.sorted:
            order = ['Green', 'Red', 'Blue', 'Yellow']

            # Rotate the list so that there isn't a bot starting
            while self.players[0].__class__.__name__ == 'Bot':
                self.players.append(self.players.pop(0))

            new_list = [self.players.pop(0)]
            last_seen_color = new_list[0].get_color()

            while self.players:
                next_color = order[(order.index(last_seen_color) + 1) % 4]

                p = None
                for player in self.players:
                    if player.get_color() == next_color:
                        p = player

                if p:
                    self.players.remove(p)
                    new_list.append(p)

                last_seen_color = next_color

            self.players = new_list
            self.sorted = True

    def add_player(self, color) -> bool:
        """
        Adds a new player to the game
        :param color: Color of the new player
        :return: Boolean of whether the player was successfully added
        """

        if color in self.available_colors:
            self.available_colors.remove(color)
            self.players.append(Player(color))
            return True

        return False

    def refresh_positions(self):
        """
        Refreshes the position's dictionary
        """
        self.positions = {}
        for player in self.players:
            self.positions[player.get_color()] = player.get_positions()

    def get_player_positions(self) -> {str: [int]}:
        """
        :return: Dictionary mapping a string to a list of integers
        """
        self.refresh_positions()
        return self.positions

    def remove_player(self, color):
        """
        Removes a player from the game
        :param color: String, color of the player
        """

        for ind, p in enumerate(self.players):
            if p.get_color() == color:
                self.players.remove(p)
                self.available_colors.append(color)

                # If it is their turn make it the next persons turn
                if self.whos_turn == color and len(self.players) > 0:
                    self.whos_turn = self.players[(ind % len(self.players))].get_color()

    def get_turn(self) -> str:
        """
        :return: String, color for whose turn it is
        """
        if not self.whos_turn:
            if len(self.players) >= 1:
                self.whos_turn = self.players[0].get_color()
        return self.whos_turn

    def next_player(self):
        """
        Moves the turn to the next player
        """
        if len(self.players) >= 1:
            flag = False
            bot = False

            for ind, p in enumerate(self.players):
                if p.get_color() == self.whos_turn and not flag:
                    player = self.players[(ind+1) % len(self.players)]
                    self.whos_turn = player.get_color()
                    if player.__class__.__name__ == 'Bot':
                        bot = True
                    flag = True

            # If this next player is a bot, then move them
            if bot:
                self.handle_bot_movement()

                # Move onto the next player
                self.next_player()

    def handle_bot_movement(self):
        """
        Handles the bots turn, updates the positions for after the turn is complete.
        """
        old_positions = copy.deepcopy(self.positions)

        # Handle the turn
        for ind, p in enumerate(self.players):
            if p.get_color() == self.whos_turn:
                self.draw_card()
                self.positions = p.handle_turn(self.positions.copy(), self.current_card())

                # Check for collision or swap messages
                self.check_for_messages(old_positions)

                while self.current_card().get_value() == Value.Two:
                    old_positions = copy.deepcopy(self.positions)
                    # Draw again and do it again until it's not a 2
                    self.draw_card()
                    self.positions = p.handle_turn(self.positions.copy(), self.current_card())

                    # Check for collision or swaps
                    self.check_for_messages(old_positions)

    def check_for_messages(self, old_positions):
        """
        Checks to see if any player has been sent home or swapped with to add the alert to their logs
        :param old_positions: {str: [int]} Positions of pieces before the move
        :return Nothing
        """
        for player in self.players:
            if player.__class__.__name__ == 'Player':
                color = player.get_color()

                for ind, pos in enumerate(old_positions[color]):
                    if pos != self.positions[color][ind]:
                        # Check if its back at start or swapped
                        if self.positions[color][ind] == constants.STARTS[color]:
                            self.add_msg(color, 'bh')
                        else:
                            self.add_msg(color, 'swapped')

    def current_card(self) -> Card:
        """
        :return: Card object of the card drawn
        """
        if self.card:
            return self.card

    def draw_card(self):
        """
        Draws a card from the deck
        """
        self.card = self.deck.draw_card()

    def get_player(self, color) -> Player:
        """
        Returns the player object that has the specified color
        :param color: String
        :return: Player object
        """
        if color:
            for p in self.players:
                if p.get_color() == color:
                    return p

    def update_player_location(self, color, positions):
        """
        Updates the locations of a player
        :param color: String, color of the player
        :param positions: Array of Integers, new positions
        """
        for p in self.players:
            if p.get_color() == color:
                p.update_positions(positions)

    def update_all_locations(self, player_pos):
        """
        Updates the locations of all players
        :param player_pos: Dictionary mapping string to array of integers {color : [positions]}
        """
        for key in player_pos.keys():
            self.update_player_location(key, player_pos[key])

    def check_win(self):
        """
        Check if any player has won the game
        """
        self.refresh_positions()
        for p in self.players:
            color = p.get_color()
            if [constants.HOMES[color]] * 4 == self.positions[color]:
                self.won = True
                self.winner = color

    def get_msg(self, color) -> str:
        """
        Gets a message for the user, if one exists
        :param color: String of the color
        :return: String of the message
        """
        if len(self.logs[color]) > 0:
            # Return the first item
            return self.logs[color].pop(0)

    def add_msg(self, color, msg):
        """
        Adds a message to a specified user
        :param color: String of the color
        :param msg: String of the message
        """
        self.logs[color].append(msg)

    def check_bot(self) -> bool:
        """
        Checks if there is at least one bot in play
        :return: Boolean
        """
        for player in self.players:
            if player.__class__.__name__ == 'Bot':
                return True

        return False

    def add_bot(self):
        """
        Adds a bot to the player list
        """
        if len(self.players) < 4:
            new_bot = Bot(self.available_colors.pop())
            self.players.append(new_bot)

    def remove_bot(self):
        """
        Removes a bot from the player list if there is one
        """
        # Remove the first bot found
        for item in self.players:
            if item.__class__.__name__ == 'Bot':
                # Add the color back to available colors
                self.available_colors.append(item.get_color())
                self.players.remove(item)
                return

    def check_full(self) -> bool:
        """
        Check if the games full
        :return: Boolean, whether the game is full
        """
        if len(self.players) == 4:
            return True
