import random


class DeckManager:

    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.decks = [
            [
                ('SEATTLE', (0, 12)),
                ('PORTLAND', (0, 11)),
                ('MEDFORD', (1, 9)),
                ('SACRAMENTO', (2, 7)),
                ('SAN FRANCISCO', (2, 6)),
                ('LOS ANGELES', (5, 3)),
                ('SAN DIEGO', (6, 2))
            ],
            [
                ('HELENA', (3, 11)),
                ('BISMARK', (7, 11)),
                ('DULUTH', (10, 11)),
                ('MINNEAPOLIS', (10, 10)),
                ('CHICAGO', (13, 9)),
                ('CINCINNATI', (15, 7)),
                ('BUFFALO', (15, 10))
            ],
            [
                ('SALT LAKE CITY', (4, 8)),
                ('DENVER', (7, 7)),
                ('OMAHA', (9, 7)),
                ('SANTA FE', (8, 4)),
                ('KANSAS CITY', (11, 6)),
                ('OKLAHOMA CITY', (11, 4)),
                ('ST. LOUIS', (13, 6))
            ],
            [
                ('PHOENIX', (7, 3)),
                ('EL PASO', (10, 1)),
                ('HOUSTON', (14, 0)),
                ('DALLAS', (13, 2)),
                ('MEMPHIS', (15, 3)),
                ('ATLANTA', (17, 2)),
                ('NEW ORLEANS', (16, 0))
            ],
            [
                ('BOSTON', (17, 10)),
                ('NEW YORK', (17, 8)),
                ('WASHINGTON', (17, 7)),
                ('RICHMOND', (18, 5)),
                ('WINSTON', (17, 4)),
                ('CHARLESTON', (19, 2)),
                ('JACKSONVILLE', (19, 0))
            ]
        ]
        self.shuffle()

    def shuffle(self):
        for deck in self.decks:
            random.shuffle(deck)

    def draw_a_starting_hand(self):
        hand = []
        for deck in self.decks:
            hand.append(deck.pop())
        return hand

    def complete_hand(self, current_hand):
        reference_decks = DeckManager().decks
        new_hand = []
        for i, deck in enumerate(reference_decks):
            has_color = False
            for card in deck:
                if card[1] in current_hand:
                    has_color = True
                    new_hand.append(card[1])
                    break
            if not has_color:
                new_hand.append(self.decks[i].pop()[1])
        return new_hand

    def remove_card_from_decks(self, card_to_remove):
        if type(card_to_remove) is tuple:
            for i, deck in enumerate(self.decks):
                for card in deck:
                    if card[1] == card_to_remove:
                        self.decks[i].remove(card)
        else:
            print('Remove card from deck not implemented for representations other than tuple.')

    def reset(self):
        self.__init__()
