from player import BasePlayer


class AdvancedPlayer(BasePlayer):

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