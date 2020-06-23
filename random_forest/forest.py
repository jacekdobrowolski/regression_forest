"""
Forest module
***********************

Module implementing random regression forest
"""

from random_forest.tree import Tree
import numpy as np
import json
import concurrent.futures


class Config(object):
    """Configuration Object, member fields must be overwritten using :meth:`create_config` after import.
    """
    def __init__(self):
        self.number_of_trees = 1
        self.data_size_for_tree = 1
    
    def create_config(self, number_of_trees, data_size_for_tree):
        """
        Configures forest
        
        Args:
            number_of_trees (int): Number of trees for the forest to contain.
            data_size_for_tree (int): Determines number of rows of training data
        that go into every tree construction. """
        self.number_of_trees = number_of_trees
        self.data_size_for_tree = data_size_for_tree


config = Config()

class Forest(object):
    """Represents random forest"""
    def __init__(self, data):
        self.out_of_bag = data
                
        with concurrent.futures.ProcessPoolExecutor() as executor:
            self.trees = list(executor.map(Tree, self.bootstrap(data)))

    def bootstrap(self, data):
        """ Randomly draws with repetitions rows form given :attr:`data`.
        Record are stored in list of :class:`np.ndarrays` form which trees are created.
        Record that were not selected can by found in :attr:`self.out_of_bag`.

        Args:
            data (:class:`pandas.DataFrame`): training data for the forest

        Returns:
            list : list of :class:`np.ndarrays` for each tree training
        """
        bootstraped_data = []
        for _ in range(config.number_of_trees):
            training_data = data.sample(config.data_size_for_tree, replace=True)
            self.out_of_bag = self.out_of_bag[~self.out_of_bag.index.isin(training_data.index)]
            bootstraped_data.append(training_data.values)
        return bootstraped_data

    def predict(self, data):
        """Calculates value predicted by the forest

        Args:
            data (:class:`np.ndarray`): data for which prediction is made

        Returns:
            float: average value of all trees predictions
        """
        prediction = 0
        for each in self.trees:
            prediction += each.predict(data)
        return prediction/len(self.trees)

