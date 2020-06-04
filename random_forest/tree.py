"""
Tree module
***********************

The core module providing building blocks of regression trees
"""

def node_factory(data, features, output, min_size: int):
    """Calls appropriate constructor dependant on data size.

    Args:
        data (pandas.DataFrame): Data from which node will be created
        features (str): Lorem opsum
        output (str): Lorem opsum
        min_size (int): Lorem opsum

    Returns:
        Leaf: Lorem opsum
    """
    if data < min_size:
        return Leaf(data, features, output, min_size)
    else:
        return Branch(data, features, output, min_size)


class Tree(object):
    def __init__(self, data, features, output, min_size):
        self.root = node_factory(data, features, output, min_size)


class Leaf(object):
    def __init__(self, data, features, output, min_size):
        self.value = data[output].mean()
        print(f'Leaf is created data: {self.value}')

    def predict(self, data):
        return self.value


class Branch(object):
    def __init__(self, data, features, output, min_size):
        print(f"Branch is created data: {data}")
        self.data = data

        self.find_best_split =  None
        self.condition = None # tuple(predictor, value) # predictor >= value

        for predictor in range(data.shape[1]):
            # sort by given predictor
            sorted_predictor = data[:, predictor].argsort()
            sorted_data = self.data[sorted_predictor]
            for value in sorted_data[:, predictor]:
                pass

        leftData = data/2
        rightData = data/2
        self.leftNode = node_factory(leftData, features, output, min_size)
        self.rightNode = node_factory(rightData, features, output, min_size)

    def predict(self, data):
        if data[self.condition.predictor] >= self.condition.value:
            self.leftNode.predict(data)
        else:
            self.rightNode.predict(data)

