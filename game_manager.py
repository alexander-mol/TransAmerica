from player import BasePlayer
from deck_manager import DeckManager
from game import Game
import pickle
import time
import logging
import matplotlib.pyplot as plt
import numpy as np


class GameManager:

    def __init__(self, player_list=None):
        if player_list is None:
            self.player_list = [BasePlayer('A'), BasePlayer('B'), BasePlayer('C')]
        self.deck_manager = DeckManager()
        with open('game-board.p', 'rb') as f:
            self.board = pickle.load(f)
        self.game = Game(self.player_list, self.board)
        logging.basicConfig(filename='log.txt',
                            filemode='w',
                            # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            format='%(message)s',
                            # datefmt='%H:%M:%S',
                            level=logging.ERROR)
        self.logger = logging.getLogger(__name__)

    def deal_objective_cards(self):
        for player in self.player_list:
            player.set_objectives(self.deck_manager.draw_a_starting_hand())

    def play(self):
        self.deal_objective_cards()
        for player in self.player_list:  # TODO MAKE THIS HAVE VARIABLE STARTING PLAYER...
            player.decide_starting_node(self.game)
        # main game loop
        done = False
        while not done:
            for player in self.player_list:  # TODO MAKE THIS HAVE VARIABLE STARTING PLAYER
                self.logger.debug(f'Player {player}: round {self.game.round_counter}, remaining objectives:'
                                  f' {[player.verbose_objectives[x] for x in player.remaining_objectives]}.')
                if player.is_done(self.game):
                    self.logger.info(f'Player {player}: round {self.game.round_counter}, finished all objectives!')
                    done = True
                    break
                edges_to_place = player.decide_edge_placement(self.game)
                self.logger.debug(f'Player {player}: round {self.game.round_counter}, places edges {edges_to_place}.')
                for edge in edges_to_place:
                    # print(edge)
                    self.board[edge[0]][edge[1]]['weight'] = 0
                if player.is_done(self.game):
                    self.logger.info(f'Player {player}: round {self.game.round_counter}, finished all objectives!')
                    done = True
                    break
            if self.logger.getEffectiveLevel() == logging.DEBUG:
                self.plot()
            self.game.round_counter += 1
        scores_dict = self.calculate_scores()
        self.logger.info(f'Scores: {scores_dict}.')
        if self.logger.getEffectiveLevel() <= logging.INFO:
            self.plot('final')
        return scores_dict

    def calculate_scores(self):
        scores_dict = {}
        for player in self.player_list:
            scores_dict[player.id] = self.game.get_remaining_distance(player.home_node, player.objectives)
        return scores_dict

    # Below this line is all for drawing images
    def get_track_edges(self):
        output = []
        for edge in self.board.edges():
            if self.board[edge[0]][edge[1]]['weight'] == 0:
                output.append(edge)
        return output

    def plot(self, title=None):
        # TODO CAN OPIMIZE THIS SO THAT ONLY DIFFS ARE ADDED TO THE IMAGE - much faster
        plt.figure(figsize=(7.44, 4.3))
        dots = 7
        for edge in self.board.edges():
            if self.board[edge[0]][edge[1]]['weight'] == 2:
                self.draw_edge(edge, dots - 3, 'y')
        edges = self.get_track_edges()
        for edge in edges:
            self.draw_edge(edge, dots, 'r')
        nodes = self.board.nodes()
        plt.scatter(x=[n[0] + n[1] * 0.5 for n in nodes], y=[n[1] * 0.866 for n in nodes], s=3)
        for player in self.player_list:
            plt.scatter(x=[o[0]+o[1]*0.5 for o in player.objectives], y=[o[1]*0.866 for o in player.objectives])
        plt.axis('off')
        plt.savefig(f'images/s-{self.game.round_counter if title is None else title}.png')
        plt.close()

    def draw_edge(self, edge, dots, color):
        x0 = edge[0][0]
        y0 = edge[0][1]
        x1 = edge[1][0]
        y1 = edge[1][1]
        plt.scatter(x=np.linspace(x0 + y0 * 0.5, x1 + y1 * 0.5, dots), y=np.linspace(y0 * 0.866, y1 * 0.866, dots),
                    s=0.6, c=color)


if __name__ == '__main__':
    start_time = time.time()
    scores_dict = {'A': 0, 'B': 0, 'C': 0}
    for _ in range(100):
        gm = GameManager()
        scores = gm.play()
        for key in scores_dict:
            scores_dict[key] += scores[key]
    print(f'Scores: {scores_dict}.')
    print(time.time() - start_time)
