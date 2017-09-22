from player import BasePlayer
from deck_manager import DeckManager
from neural_network import NeuralNetwork
import numpy as np
import copy

class OptimalPlayer(BasePlayer):
    def decide_starting_node(self, game):
        from game_manager import GameManager
        obj_scores = []
        gm_temp = GameManager()
        for obj in self.objectives:
            gm_temp.reset(game.player_list, reset_players=False)
            self.home_node = obj
            self.update_target_order(game)
            scores = gm_temp.main_game_loop()
            player_score_margin = min([x[1] for x in scores.items() if x[0] is not self.id]) - scores[self.id]
            obj_scores.append((obj, player_score_margin))
            for player in game.player_list:
                player.remaining_objectives = copy.copy(player.objectives)
        obj_scores.sort(key=lambda x: -x[1])
        self.home_node = obj_scores[0][0]
        print(self.home_node, self.verbose_objectives[self.home_node])
        self.update_target_order(game)
        return self.home_node

class MonteCarloPlayer(BasePlayer):
    def __init__(self, id, trial_runs_per_node=10):
        super().__init__(id)
        self.trial_runs_per_node = trial_runs_per_node

    def decide_starting_node(self, game):
        from game_manager import GameManager
        obj_scores = {}
        gm_temp = GameManager()
        for obj in self.objectives:
            obj_scores[obj] = 0
            for _ in range(self.trial_runs_per_node):
                new_player_list = self.create_new_player_list(game, obj)
                gm_temp.reset(new_player_list, reset_players=False)
                scores = gm_temp.main_game_loop()
                player_score_margin = min([x[1] for x in scores.items() if x[0] is not self.id]) - scores[self.id]
                obj_scores[obj] += player_score_margin
        obj_scores = list(obj_scores.items())
        obj_scores.sort(key=lambda x: -x[1])
        self.data = obj_scores
        self.home_node = obj_scores[0][0]
        # print(self.home_node, self.verbose_objectives[self.home_node])
        self.update_target_order(game)
        return self.home_node

    def create_new_player_list(self, game, self_home_node):
        new_player_list = []
        dm = self.create_new_deck_manager(game)
        for player in game.player_list:
            if player.id is self.id:
                new_self = MonteCarloPlayer(id=self.id)
                new_self.objectives = self.objectives
                new_self.remaining_objectives = copy.copy(self.objectives)
                new_self.home_node = self_home_node
                new_self.update_target_order(game)
                new_player_list.append(new_self)
                continue
            new_base_player = BasePlayer(id=player.id)
            new_base_player.objectives = dm.complete_hand([player.home_node])
            new_base_player.remaining_objectives = copy.copy(new_base_player.objectives)
            if player.home_node is None:
                new_base_player.decide_starting_node(game)
            else:
                new_base_player.home_node = player.home_node
            new_base_player.update_target_order(game)
            new_player_list.append(new_base_player)
        return new_player_list

    def create_new_deck_manager(self, game):
        dm = DeckManager()
        for player in game.player_list:
            if player.home_node is None:
                continue
            dm.remove_card_from_decks(player.home_node)
            if player.id is self.id:
                for card in self.objectives:
                    dm.remove_card_from_decks(card)
        return dm

class EmpiricalTopLeftPlayer(BasePlayer):
    def decide_starting_node(self, game):
        green_taken = False
        blue_taken = False
        for player in game.player_list:
            if player.id is self.id:
                continue
            if player.home_node in ['SEATTLE', 'PORTLAND', 'MEDFORD', 'SACRAMENTO', 'SAN FRANCISCO', 'LOS ANGELES',
                                    'SAN DIEGO']:
                green_taken = True
            if player.home_node in ['BUFFALO', 'CINCINNATI', 'CHICAGO', 'DULUTH', 'BISMARK', 'MINNEAPOLIS', 'HELENA']:
                blue_taken = True
        starting_string = None
        if green_taken and blue_taken:
            self.home_node = self.objectives[2]
        else:
            objective_strings = self.verbose_objectives.values()
            if 'SEATTLE' in objective_strings and not green_taken:
                starting_string = 'SEATTLE'
            elif 'BUFFALO' in objective_strings and not blue_taken:
                starting_string = 'BUFFALO'
            elif 'PORTLAND' in objective_strings and not green_taken:
                starting_string = 'PORTLAND'
            elif 'CINCINNATI' in objective_strings and not blue_taken:
                starting_string = 'CINCINNATI'
            elif not green_taken:
                self.home_node = self.objectives[0]
            else:
                self.home_node = game.find_central_node(self.objectives)
        if starting_string is not None:
            for key in self.verbose_objectives:
                if self.verbose_objectives[key] == starting_string:
                    self.home_node = key
        self.update_target_order(game)
        return self.home_node


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