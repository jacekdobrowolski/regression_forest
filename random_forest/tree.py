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

    def predict(self, data):
        print("predict tree is called")
        return self.root.predict(data)


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
    if (training_data.shape[0]) < min_size:
        return Leaf(training_data, min_size)
    else:
        return Branch(training_data, min_size)


class Leaf(object):
    def __init__(self, training_data, min_size):
        self.value = training_data[:,OUTPUT_INDEX].mean()

    def predict(self, data):
        return self.value
        print("predict leaf is called")

    def __repr__(self):
        return f"Leaf: {self.value}"

class Branch(object):
    def __init__(self, training_data, min_size):
        self.training_data = training_data
        self.best_split = None
        def SSR(a):
            a = a[:, OUTPUT_INDEX].flatten()
            sum = 0
            mean = a.mean()
            for i in a:
                sum +=(mean - i)**2
            return sum

        min_SSR = SSR(training_data)
        for predictor in range(training_data.shape[1] - 1):
            # sort by given predictor
            sorted_training_data = self.training_data[training_data[:, predictor].argsort()]
            # iterate over unique value entry's
            for i in np.unique(sorted_training_data[:,predictor], return_index=True)[1][:-1]:
                # SSR should be calculated for value based split not index one
                split = Condition(index=predictor, value=sorted_training_data[i, predictor])
                left_data, right_data = self.split_training_data_on_value(split)
                current_ssr = SSR(left_data) + SSR(right_data)
                if current_ssr < min_SSR:
                    min_SSR = current_ssr
                    self.best_split = split
        left_data, right_data = self.split_training_data_on_value(self.best_split)
        self.leftNode = create_node(left_data, min_size)
        self.rightNode = create_node(right_data, min_size)
        
    def __repr__(self):
        return f"""
        Branch:
            if <= {self.best_split.index}_{self.best_split.value}:
                {self.leftNode}
            else:
                {self.rightNode}  
        """

    def split_training_data_on_value(self, condition: Condition):
        return self.training_data[np.argwhere(self.training_data[:, condition.index] <= condition.value).flatten()], \
                    self.training_data[np.argwhere(self.training_data[:, condition.index] > condition.value).flatten()]

    def predict(self, data):
        print("predict branch is called")
        if data[self.best_split.index] <= self.best_split.value:
            return self.leftNode.predict(data)
        else:
            return self.rightNode.predict(data)
            

if __name__ == "__main__":
    training_data = np.array([[1.0,   6.5,  2.0 ], [0.0,   6.35, 2.18], [0.0,   6.2,  2.19],
                     [1.0,   6.05, 1.68], [1.0,   5.9,  1.5 ], [0.0,   5.74, 1.64],
                     [0.0,   5.59, 1.62], [0.0,   5.44, 1.56], [0.0,   5.3,  1.54],
                     [0.0,   5.26, 1.82], [0.0,   5.23, 1.86], [0.0,   5.21, 1.89]])
    myTree = Tree(training_data, 4)
    print(training_data)
    print(myTree.root)

    test_data = np.array([0.0,   5.23])

    print(f"\nprediction: {myTree.predict(test_data)}\n")
