from random_forest.tree import Tree
import numpy as np

class Forest(object):
    def __init__(self, training_data, min_size):
        self.trees = []
        self.trees.append(Tree(training_data, min_size))

    def predict(self, data):
        predictions = []
        for each in self.trees:
            predictions.append(each.predict())
        return np.asarray(predictions).mean()