from player import BasePlayer
from advanced_player import AdvancedPlayer, LeftPlayer, RightPlayer, NorthPlayer, SouthPlayer
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
            self.player_list = [BasePlayer('A'), BasePlayer('B'), BasePlayer('C'), BasePlayer('D')]
        self.deck_manager = DeckManager()
        with open('game-board.p', 'rb') as f:
            self.board = pickle.load(f)
        with open('board_nodes_only.p', 'rb') as f:
            self.board_track_only = pickle.load(f)
        self.game = Game(self.player_list, self.board, self.board_track_only)
        logging.basicConfig(filename='log.txt',
                            filemode='w',
                            # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            format='%(message)s',
                            # datefmt='%H:%M:%S',
                            level=logging.ERROR)
        self.logger = logging.getLogger(__name__)

    def play_repeated(self, player_list, num_games):
        start_time = time.time()
        self.reset(player_list)
        print(f'Evaluating {num_games} runs for player types: {[type(p) for p in self.player_list]}.')
        scores_dict = {}
        # track_location_count = {}
        # for edge in self.board.edges():
        #     track_location_count[edge] = 0
        for player in player_list:
            scores_dict[player.id] = 0
        for _ in range(num_games):
            self.reset(player_list)
            scores = self.play()
            for key in scores_dict:
                scores_dict[key] += scores[key]
            # for edge in self.board_track_only.edges():
            #     track_location_count[edge] += 1
        print(f'Scores: {scores_dict}.')
        fitness = 1 - (scores_dict['A'] / min([x[1] for x in list(scores_dict.items()) if x[0] is not 'A']))
        print(f'Fitness of A: {fitness}.')
        print(f'Total runtime: {round(time.time() - start_time, 3)}s, '
              f'time per game: {round((time.time() - start_time)/num_games, 4)}s.')
        # track_location_count = list(track_location_count.items())
        # track_location_count.sort(key=lambda x: x[1], reverse=True)
        # with open('track_location_count.p', 'wb') as f:
        #     pickle.dump(track_location_count, f)
        # print(track_location_count)
        print('---------------------------------------------------------')

    def reset(self, player_list):
        for player in player_list:
            player.reset()
        self.player_list = player_list
        self.deck_manager = DeckManager()
        with open('game-board.p', 'rb') as f:
            self.board = pickle.load(f)
        with open('board_nodes_only.p', 'rb') as f:
            self.board_track_only = pickle.load(f)
        self.game = Game(self.player_list, self.board, self.board_track_only)

    def deal_objective_cards(self):
        for player in self.player_list:
            player.set_objectives(self.deck_manager.draw_a_starting_hand())

    def play(self):
        self.deal_objective_cards()
        for player in self.player_list:  # TODO MAKE THIS HAVE VARIABLE STARTING PLAYER...
            starting_node = player.decide_starting_node(self.game)
            self.logger.info(f'Player {player} chooses starting node: {starting_node}.')
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
                # self.game.lay_track(edges_to_place)
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

    def plot(self, title=None):
        # TODO CAN OPIMIZE THIS SO THAT ONLY DIFFS ARE ADDED TO THE IMAGE - much faster
        plt.figure(figsize=(7.44, 4.3))
        dots = 7
        for edge in self.board.edges():
            if self.board[edge[0]][edge[1]]['weight'] == 2:
                self.draw_edge(edge, dots - 3, 'y')
        edges = self.board_track_only.edges()
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
    # start_time = time.time()
    # scores_dict = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    # for _ in range(10000):
    #     gm = GameManager()
    #     scores = gm.play()
    #     for key in scores_dict:
    #         scores_dict[key] += scores[key]
    # print(f'Scores: {scores_dict}.')
    # fitness = 1 - (scores_dict['A'] / min([x[1] for x in list(scores_dict.items()) if x[0] is not 'A']))
    # print(f'Fitness: {fitness}.')
    # print(time.time() - start_time)
    gm = GameManager()
    player_list = [BasePlayer('A'), BasePlayer('B'), BasePlayer('C'), BasePlayer('D')]
    gm.play_repeated(player_list, 100)
