"""
Tree module
***********************

The core module providing building blocks of regression trees
"""

import numpy as np
from collections import namedtuple

# Index of a feature that will be predicted
OUTPUT_INDEX = -1

Condition = namedtuple("Condition", "index value")


class Tree(object):
    def __init__(self, training_data, min_size):
        self.root = create_node(training_data, min_size)


def create_node(training_data, min_size):
    """Calls appropriate constructor dependant on training_data size.

    Args:
        training_data (pandas.training_DataFrame): training_Data from which node will be created
        features (str): Lorem ipsum
        output (str): Lorem ipsum
        min_size (int): Lorem ipsum

    Returns:
        Leaf: Lorem ipsum
    """
    if training_data < min_size:
        return Leaf(training_data, min_size)
    else:
        return Branch(training_data, min_size)


class Leaf(object):
    def __init__(self, training_data, min_size):
        self.value = training_data[OUTPUT_INDEX].mean()
        print(f'Leaf is created training_data: {self.value}')

    def predict(self, training_data):
        return self.value


class Branch(object):
    def __init__(self, training_data, min_size):
        print(f"Branch is created training_data: {training_data}")
        self.training_data = training_data
        self.best_split = None
        def SSR(a): return ((a.mean() - a)**2).sum()
        min_SSR = -1.0
        for predictor in range(training_data.shape[1] - 1):
            # sort by given predictor
            sorted_training_data = self.training_data[training_data[:, predictor].argsort(
            )]
            # finding best split value
            for i in range(1, sorted_training_data.shape[0]):
                # SSR should be calculated for value based split not index one
                split = Condition(
                    index=predictor, value=sorted_training_data[i, predictor])
                left_data, right_data = self.split_training_data_on_value(
                    split)
                SSR = SSR(left_data) + SSR(right_data)
                if SSR < min_SSR:
                    min_SSR = SSR
                    self.best_split = Condition(
                        index=predictor, value=sorted_training_data[i, predictor])

        left_data, right_data = self.split_training_data_on_value(
            self.best_split)
        self.leftNode = create_node(left_data, min_size)
        self.rightNode = create_node(right_data, min_size)

    def split_training_data_on_value(self, condition: Condition):
        return self.training_data[np.argwhere(self.training_data[:, condition.predictor] <= condition.value).flatten()], \
            self.training_data[np.argwhere(
                self.training_data[:, condition.predictor] > condition.value).flatten()]

    def predict(self, training_data):
        if training_data[self.best_split.index] <= self.best_split.value:
            self.leftNode.predict(training_data)
        else:
            self.rightNode.predict(training_data)
