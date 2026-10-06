import random

class CardDeck:
    def __init__(self):    # self is the reference to the current object.
        self.reset()       # call the reset method for the current object.

    def reset(self):
        suits = ("Clubs", "Spades", "Hearts", "Diamonds")
        faces = ("Jack", "Queen", "King", "Ace")
        numbered = (2, 3, 4, 5, 6, 7, 8, 9, 10)
        self.deck = set()     # The self insures the deck variable is a visible object attribute.
        for suit in suits:
            for card in faces + numbered:
                self.deck.add( f"{card} of {suit}" )     # this is an f-string (f for formatting).

    def draw(self):
        card = random.choice(list(self.deck))
        self.deck.remove(card)
        return card

    def __len__(self):
        return len(self.deck)