from random_forest.tree import Tree
import numpy as np
import json
import concurrent.futures


class Config(object):
    def __init__(self):
        self.number_of_trees = 1
        self.data_size_for_tree = 1
    
    def create_config(self, number_of_trees, data_size_for_tree):
        self.number_of_trees = number_of_trees
        self.data_size_for_tree = data_size_for_tree


config = Config()

class Forest(object):
    def __init__(self, data):
        self.out_of_bag = data
                
        with concurrent.futures.ProcessPoolExecutor() as executor:
            self.trees = list(executor.map(Tree, self.bootstrap(data)))

    def bootstrap(self, data):
        bootstraped_data = []
        for _ in range(config.number_of_trees):
            training_data = data.sample(config.data_size_for_tree, replace=True)
            self.out_of_bag = self.out_of_bag[~self.out_of_bag.index.isin(training_data.index)]
            bootstraped_data.append(training_data.values)
        return bootstraped_data

    def predict(self, data):
        prediction = 0
        for each in self.trees:
            prediction += each.predict(data)
        return prediction/len(self.trees)

