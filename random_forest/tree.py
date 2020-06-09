"""
Tree module
***********************

Module implementing regression tree
"""

import numpy as np
import random
from collections import namedtuple


OUTPUT_INDEX = -1
# Index of a feature that will be predicted

Condition = namedtuple("Condition", "index value")
""" Contains information about predictor index and treshold. Needed for branching """

class Config(object):
    """Configuration for using tree module.
    Overwrite them after importing module to configure tree building variables.

    Attributes:
        min_split_size (int): Minimum size required for set of date to br further branched
        number_of_predicotrs_to_draw (int): Number of predictors which will be randomly drawn, \\
                                                from which the best split condition will be selected.
    """
    def __init__(self):
        self.min_split_size = 1
        self.number_of_predictors_to_draw = 1

# creates default config to be overwritten by calling script
config = Config()

class Tree(object):
    """Object representing regression tree

    Args:
        training_data (np.ndarray): Data from which Tree will be created
    """
    def __init__(self, training_data):
        self.training_data = training_data
        self.root = create_node(training_data)

    def predict(self, data) -> float:
        """Calculates regression tree prediction

        Args:
            data (np.ndarray): data for which prediction will be made.
            Single dimension array. Can be one field shorter than training data.

        Returns:
            float: Prediction
        """
        return self.root._predict(data)

    def __repr__(self):
        return f"""
        min_split_size: {config.min_split_size}
        number_of_predictors_to_draw: {config.number_of_predictors_to_draw}
        {self.root}
        """


def create_node(training_data):
    """Calls appropriate constructor dependant on training_data size.

    Args:
        training_data (np.ndarray): Data from which node will be created

    Returns:
        :class:`Branch`, :class:`Leaf`: Node
        
    """
    if (training_data.shape[0]) < config.min_split_size:
        return Leaf(training_data)
    else:
        return Branch(training_data)


class Leaf(object):
    """ Represent Leaf of the Tree. Contains possible values for prediction """
    def __init__(self, training_data):
        self.value = training_data[:,OUTPUT_INDEX].mean()

    def _predict(self, data) -> float:
        return self.value

    def __repr__(self):
        return f"Leaf: {self.value}"


class Branch(object):
    """ Represents Branch of the Tree. Contains :class:`Condition` to select appropriate subnode (:class:`Branch` or :class:`Leaf`) """
    def __init__(self, training_data):
        self.best_split = None
        self.find_best_split(training_data)
        left_data, right_data = self.split_data_on_value(training_data, self.best_split)
        self.left_node = create_node(left_data)
        self.right_node = create_node(right_data)
        
    def _predict(self, data) -> float:
        if data[self.best_split.index] <= self.best_split.value:
            return self.left_node._predict(data)
        else:
            return self.right_node._predict(data)

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
        
        for predictor in self.draw_predictors(training_data):
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

    def draw_predictors(self, training_data):
        predictors = [i for i in range(training_data.shape[1] - 1)]
        return random.sample(predictors, config.number_of_predictors_to_draw)

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
