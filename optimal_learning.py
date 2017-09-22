import random
import numpy as np
from scipy.stats import invgauss


class OptimalSampler:

    def __init__(self, options):
        self.options = options
        self.tracking_data = {}

    def evaluate(self, initial_probes=3, confidence_level=0.99):
        if confidence_level > 0 or confidence_level < 0:
            print('Error: Confidence level not between 0 and 1.')
            return
        for option in self.options:
            estimates = []
            for _ in range(initial_probes):
                estimates.append(option.get_sample())
            self.tracking_data[option] = {'times_sampled': initial_probes, 'estimated_mean': self.mean(estimates),
                                          'estimated_stdev': self.stdev(estimates)}

    def prune_options(self):
        best_seen_mean = -1e31
        best_seen_option = None
        for option in self.tracking_data:
            if option['estimated_mean'] > best_seen_mean:
                best_seen_mean = option['estimated_mean']
                best_seen_option = option
        for option in self.tracking_data:
            if option is best_seen_option:
                continue
            if



    @staticmethod
    def mean(values):
        return sum(values) / len(values)

    def stdev(self, values, mean=None):
        if mean is None:
            mean = self.mean(values)
        return self.mean([(x - mean) ** 2 for x in values]) ** 0.5

class ExampleOption:
    def __init__(self):
        self.true_mean = random.randint(0, 100)
        self.sampling_stdev = random.randint(0, 100)

    def get_sample(self):
        return np.random.normal(self.true_mean, self.sampling_stdev)

if __name__ == '__main__':
    option = ExampleOption()
    print(option.get_sample())