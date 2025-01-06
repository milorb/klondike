import random

from card import Card, CardAssets

class Board:
    """
    main gameplay scene layout:
    |[draw][dump]      [pile][pile][pile][pile]
    |[tab0][tab1][tab2][tab3][tab4][tab5][tab6]
    |
    |     
    """

    def __init__(self):

        random.seed()

        self.ranks = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
        self.suits = ["heart", "spade", "diamond", "club"]

        self.deck = [(rank, suit) for rank in self.ranks for suit in self.suits]

        card_assets = CardAssets()

        self.card_back = card_assets.card_back
        self.card_images = card_assets.get_card_images(self.ranks, self.suits, scale=2)

        random.shuffle(self.deck)

    def get_card_from_deck(self):
        if self.deck:
            rank_and_suit = self.deck.pop(-1)
            rank = rank_and_suit[0]
            suit = rank_and_suit[1]

            card = Card(self.card_images[rank][suit], rank, suit)

            return card
        

