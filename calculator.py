from game_manager import GameManager
from game import Game
from deck_manager import DeckManager
from advanced_player import MonteCarloPlayer
from player import BasePlayer

def convert_city_name_to_coordinates(city_name):
    dm = DeckManager()
    for deck in dm.decks:
        for city in deck:
            if city[0].lower() == city_name.lower():
                return city[1]

def calculate(me, player_list, home_node_list, my_cards_list, trial_runs_per_node=100):
    gm = GameManager(player_list)
    for i, player in enumerate(gm.player_list):
        if player is me or player.home_node is not None:
            continue
        player.home_node = home_node_list[i]
        player.update_target_order(gm.game)
    me.objectives = []
    me.remaining_objectives = []
    card_dict = {}
    for card in my_cards_list:
        coords = convert_city_name_to_coordinates(card)
        card_dict[coords] = card
        me.objectives.append(coords)
        me.remaining_objectives.append(coords)

    me.trial_runs_per_node = trial_runs_per_node
    me.decide_starting_node(gm.game)
    return [(card_dict[x[0]], x[1]) for x in me.data]

me = MonteCarloPlayer('Me')
player_list = [me, BasePlayer('B'), BasePlayer('C'), BasePlayer('D')]
home_node_list = [None, None, None, None]
my_cards_list = ['San Francisco', 'Houston', 'Richmond', 'Helena', 'Salt Lake City']

print(calculate(me, player_list, home_node_list, my_cards_list))
