"""
Tree module
***********************

The core module implementing regression tree
"""

import numpy as np
from collections import namedtuple

# Index of a feature that will be predicted
OUTPUT_INDEX = -1

Condition = namedtuple("Condition", "index value")

class Tree(object):
    def __init__(self, training_data, min_size):
        self.root = create_node(training_data, min_size)

    def predict(self, data):
        return self.root.predict(data)


def create_node(training_data, min_size):
    """Calls appropriate constructor dependant on training_data size.

    Args:
        training_data (pandas.DataFrame): Data from which node will be created
        features (str): Lorem ipsum
        output (str): Lorem ipsum
        min_size (int): Lorem ipsum

    Returns:
        Leaf: Lorem ipsum
    """
    if (training_data.shape[0]) < min_size:
        return Leaf(training_data, min_size)
    else:
        return Branch(training_data, min_size)


class Leaf(object):
    def __init__(self, training_data, min_size):
        self.value = training_data[:,OUTPUT_INDEX].mean()

    def predict(self, data):
        return self.value

    def __repr__(self):
        return f"Leaf: {self.value}"


class Branch(object):
    def __init__(self, training_data, min_size):
        self.best_split = None
        self.find_best_split(training_data)
        left_data, right_data = self.split_data_on_value(training_data, self.best_split)
        self.left_node = create_node(left_data, min_size)
        self.right_node = create_node(right_data, min_size)
        
    def predict(self, data):
        if data[self.best_split.index] <= self.best_split.value:
            return self.left_node.predict(data)
        else:
            return self.right_node.predict(data)

    def split_data_on_value(self, data, condition: Condition):
        return data[np.argwhere(data[:, condition.index] <= condition.value).flatten()], \
                    data[np.argwhere(data[:, condition.index] > condition.value).flatten()]
    
    def find_best_split(self, training_data):
        min_ssr = self.ssr(training_data)
        for predictor in range(training_data.shape[1] - 1):
            # sort by given predictor
            sorted_training_data = training_data[training_data[:, predictor].argsort()]
            # iterate over unique value entry's
            for i in np.unique(sorted_training_data[:,predictor], return_index=True)[1][:-1]:
                split = Condition(index=predictor, value=sorted_training_data[i, predictor])
                left_data, right_data = self.split_data_on_value(training_data, split)
                current_ssr = self.ssr(left_data) + self.ssr(right_data)
                if current_ssr < min_ssr:
                    min_ssr = current_ssr
                    self.best_split = split
        assert self.best_split is not None

    def ssr(self, array):
            array = array[:, OUTPUT_INDEX].flatten()
            sum = 0
            mean = array.mean()
            for i in array:
                sum +=(mean - i)**2
            return sum

    def __repr__(self):
        return f"""
        Branch:
            if <= {self.best_split.index}_{self.best_split.value}:
                {self.left_node}
            else:
                {self.right_node}  
        """
