import constants

"""
TODO:
Needs to behave similarly to the player class. Will need an extra function for getting a card, calculating and selecting
positions. and then the game class will have to take that to reflect the bots 'turn'.

Game will have to check if the current turn is for a bot, if so then:
Game will need to update the positions 
then Give the bot a drawn card
Bot class will take the card and calculate possible moves
A move will be selected at random, update the positions
Will I need to update all positions here???? Or will I do that in game class to handle people sending other people home
Update the positions back on the game to reflect its move 
"""


class Bot:
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
