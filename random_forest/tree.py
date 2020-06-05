"""
Tree module
***********************

Module implementing regression tree
"""

import numpy as np
from collections import namedtuple

OUTPUT_INDEX = -1
""" Index of a feature that will be predicted """

Condition = namedtuple("Condition", "index value")
""" Contains information about predictor index and treshold. Needed for branching """

class Tree(object):
    """Object representing regression tree"""
    def __init__(self, training_data, min_size):
        """ 
        Args:
            training_data (np.ndarray): Data from which Tree will be created
            min_size (int): Minimum size required for set of date to br further branched
        """
        self.root = create_node(training_data, min_size)

    def predict(self, data) -> float:
        """Calculates regression tree prediction

        Args:
            data (np.ndarray): data for which prediction will be made.
            Single dimension array. Can be one field shorter than training data.

        Returns:
            float: Prediction
        """
        return self.root.predict(data)


def create_node(training_data, min_size):
    """Calls appropriate constructor dependant on training_data size.

    Args:
        training_data (np.ndarray): Data from which node will be created
        min_size (int): Minimum size required for set of date to br further branched

    Returns:
        Node: Branch or Leaf
    """
    if (training_data.shape[0]) < min_size:
        return Leaf(training_data, min_size)
    else:
        return Branch(training_data, min_size)


class Leaf(object):
    """ Represent Leaf of the Tree. Contains possible values for prediction """
    def __init__(self, training_data, min_size):
        self.value = training_data[:,OUTPUT_INDEX].mean()

    def predict(self, data) -> float:
        return self.value

    def __repr__(self):
        return f"Leaf: {self.value}"


class Branch(object):
    """ Represents Branch of the Tree. Contains condition to select appropriate subnode """
    def __init__(self, training_data, min_size):
        self.best_split = None
        self.find_best_split(training_data)
        left_data, right_data = self.split_data_on_value(training_data, self.best_split)
        self.left_node = create_node(left_data, min_size)
        self.right_node = create_node(right_data, min_size)
        
    def predict(self, data) -> float:
        if data[self.best_split.index] <= self.best_split.value:
            return self.left_node.predict(data)
        else:
            return self.right_node.predict(data)

    def split_data_on_value(self, data, condition: Condition):
        """Splits np.ndarray using condition

        Args:
            data (np.array): data to be splitted
            condition (Condition): condition of split

        Returns:
            left_node(np.ndarray): array lesser or equal to condition
            right_node(np.ndarray): array greater than condition
        """
        return data[np.argwhere(data[:, condition.index] <= condition.value).flatten()], \
                    data[np.argwhere(data[:, condition.index] > condition.value).flatten()]
    
    def find_best_split(self, training_data):
        """Finds condition for split that gives lowest Residual Sum of Squares

        Args:
            training_data (np.ndarray): input data
        """
        min_rss = self.rss(training_data)
        for predictor in range(training_data.shape[1] - 1):
            # sort by given predictor
            sorted_training_data = training_data[training_data[:, predictor].argsort()]
            # iterate over unique value entry's
            for i in np.unique(sorted_training_data[:,predictor], return_index=True)[1][:-1]:
                split = Condition(index=predictor, value=sorted_training_data[i, predictor])
                left_data, right_data = self.split_data_on_value(training_data, split)
                current_rss = self.rss(left_data) + self.rss(right_data)
                if current_rss < min_rss:
                    min_rss = current_rss
                    self.best_split = split
        assert self.best_split is not None

    def rss(self, array) -> float:
        """Residual Sum of Squares

        Args:
            array (np.ndarray): input array 

        Returns:
            float: Residual Sum of Squares
        """
        array = array[:, OUTPUT_INDEX].flatten()
        mean = array.mean()
        return np.sum((array - mean)**2)

    def __repr__(self):
        return f"""
        Branch:
            if <= {self.best_split.index}_{self.best_split.value}:
                {self.left_node}
            else:
                {self.right_node}  
        """
