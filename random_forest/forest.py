from random_forest.tree import Tree
import numpy as np

class Forest(object):
    def __init__(self, training_data, min_size):
        self.trees = []
        self.trees.append(Tree(training_data))

    def predict(self, data):
        for each in self.trees:
            predition += each.predict()
        return predition/len(self.trees)