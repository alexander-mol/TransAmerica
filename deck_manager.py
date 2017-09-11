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

    def reset(self):
        self.__init__()
