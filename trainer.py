from genetic_algorithm import GeneticAlgorithm
from game_manager import GameManager
from player import BasePlayer
from advanced_player import LearningPlayer
import numpy as np
import pickle
import time
import random


def fitness_evaluator(array):
    num_estimates = 100
    base_player_list = [BasePlayer('B'), BasePlayer('C'), BasePlayer('D')]
    gm = GameManager()
    return gm.play_repeated(base_player_list + [LearningPlayer('A', array)], num_estimates, seed=0)

if __name__ == '__main__':
    with open('pop_cache.p', 'rb') as f:
        init_pop = pickle.load(f)
    start_time = time.time()
    ga = GeneticAlgorithm(181, fitness_evaluator, 100, 1000, mutation_rate=0.03, mutation_severity=0.3, num_processes=7)
    vec = ga.evolve(hot_start_population=init_pop)
    # vec = ga.evolve()
    with open(time.strftime('%m%d%H%M')+'.p', 'wb') as f:
        pickle.dump(vec, f)
    print(f'Time: {time.time() - start_time} s')
