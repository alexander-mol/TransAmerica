from player import BasePlayer
from neural_network import NeuralNetwork
import numpy as np

class LearningPlayer(BasePlayer):
    def __init__(self, id, params):
        self.nn = NeuralNetwork([16, 8, 5])
        self.nn.set_parameters(params)
        super().__init__(id)

    def decide_starting_node(self, game):
        if game.player_list[0].id is 'A':
            return super().decide_starting_node(game)
        input_vector = []
        for player in game.player_list:
            if player is not self:
                input_vector.extend([player.home_node[0], player.home_node[1]])
        for obj in self.objectives:
            input_vector.extend([obj[0], obj[1]])
        output = self.nn.feed_forward(np.array(input_vector))
        self.home_node = self.objectives[np.argmax(output)]
        self.update_target_order(game)
        return self.home_node

class FarAwayPlayer(BasePlayer):
    def decide_starting_node(self, game):
        if game.player_list[0].id is 'A':
            return super().decide_starting_node(game)
        objective_dist_score = dict([(obj, 0) for obj in self.objectives])
        for obj in self.objectives:
            for player in game.player_list:
                if player is not self:
                    objective_dist_score[obj] += game.dist_est(obj, player.home_node)
        objective_dist_score = list(objective_dist_score.items())
        objective_dist_score.sort(key=lambda x: x[1], reverse=True)
        self.home_node = objective_dist_score[0][0]
        self.update_target_order(game)
        return self.home_node

class CenterPlayer(BasePlayer):
    def decide_starting_node(self, game):
        self.home_node = game.find_central_node(self.objectives)
        self.update_target_order(game)
        return self.home_node

class LeftPlayer(BasePlayer):
    def decide_starting_node(self, game):
        self.objectives.sort(key=lambda x: x[0]+x[1]*0.5)
        self.home_node = self.objectives[0]
        self.update_target_order(game)
        return self.home_node

class RightPlayer(BasePlayer):
    def decide_starting_node(self, game):
        self.objectives.sort(key=lambda x: x[0]+x[1]*0.5, reverse=True)
        self.home_node = self.objectives[0]
        self.update_target_order(game)
        return self.home_node

class NorthPlayer(BasePlayer):
    def decide_starting_node(self, game):
        self.objectives.sort(key=lambda x: x[1], reverse=True)
        self.home_node = self.objectives[0]
        self.update_target_order(game)
        return self.home_node

class SouthPlayer(BasePlayer):
    def decide_starting_node(self, game):
        self.objectives.sort(key=lambda x: x[1])
        self.home_node = self.objectives[0]
        self.update_target_order(game)
        return self.home_node