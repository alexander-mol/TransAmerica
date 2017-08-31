import random
import networkx as nx
import copy
import logging

class BasePlayer:

    def __init__(self, id):
        self.id = id
        self.objectives = []
        self.remaining_objectives = []
        self.verbose_objectives = {}
        self.home_node = None
        self.target_order = None
        self.logger = logging.getLogger(__name__)

    def set_objectives(self, objectives):
        self.verbose_objectives = {}
        for objective in objectives:
            self.objectives.append(objective[1])
            self.remaining_objectives.append(objective[1])
            self.verbose_objectives[objective[1]] = objective[0]

    def decide_starting_node(self, game):
        self.home_node = random.choice(self.objectives)
        self.update_target_order(game) # TEMPORARY
        return self.home_node

    def decide_edge_placement(self, game):
        # self.update_target_order(game)
        track_to_place = []
        track_weight = 0
        for target in self.target_order:
            potential_edges = game.get_nonzero_edges_shortest_path(game.board, self.home_node, target)[:2]
            edge_weights = game.edge_weights(potential_edges)
            for i, edge in enumerate(potential_edges):
                if track_weight + edge_weights[i] <= 2:
                    track_to_place.append(edge)
                    track_weight += edge_weights[i]
                    game.lay_track([edge])
                else:
                    break
            if track_weight == 2:
                return track_to_place
        self.logger.info(f'Player {self}, round: {game.round_counter}, only placed one point worth of track.')
        return track_to_place

    def update_target_order(self, game):
        dist_list = [(x, nx.astar_path_length(game.board, self.home_node, x))
                     for x in self.remaining_objectives]
        dist_list.sort(key=lambda x: x[1])
        self.target_order = [x[0] for x in dist_list if x[1] > 0]

    def is_done(self, game):
        for objective in self.remaining_objectives:
            if nx.has_path(game.board_track_only, self.home_node, objective):
                self.remaining_objectives.remove(objective)
        if len(self.remaining_objectives) == 0:
            return True
        return False

    def __str__(self):
        return self.id
