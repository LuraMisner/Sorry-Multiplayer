from card import Card
from card_value import Value
from random import *


class Deck:
    def __init__(self):
        self.deck = []

        # Add each card 4 times to the deck
        for i in range(4):
            new_card = Card(Value.One)
            self.deck.append(new_card)
            new_card = Card(Value.Two)
            self.deck.append(new_card)
            new_card = Card(Value.Three)
            self.deck.append(new_card)
            new_card = Card(Value.Four)
            self.deck.append(new_card)
            new_card = Card(Value.Five)
            self.deck.append(new_card)
            new_card = Card(Value.Seven)
            self.deck.append(new_card)
            new_card = Card(Value.Eight)
            self.deck.append(new_card)
            new_card = Card(Value.Ten)
            self.deck.append(new_card)
            new_card = Card(Value.Eleven)
            self.deck.append(new_card)
            new_card = Card(Value.Twelve)
            self.deck.append(new_card)
            new_card = Card(Value.Sorry)
            self.deck.append(new_card)

        # Shuffles the deck
        shuffle(self.deck)

    def draw_card(self) -> Card:
        # If the deck is empty, shuffle it and refill it
        if len(self.deck) == 0:
            self.__init__()

        # Otherwise, pick the last card from the deck to remove
        drawing_card = self.deck.pop()
        return drawing_card
