from random_forest import LEAF_SIZE

def nodeFactory(data):
    if data <= LEAF_SIZE:
        return Leaf(data)
    else:
        return Branch(data)

class Tree(object):
    def __init__(self, data):
        self.root = nodeFactory(data)

class Leaf(object):
    def __init__(self, data):
        print(f'Leaf is created data: {data}')

class Branch(object):
    def __init__(self, data):
        print(f"Branch is created data: {data}")
        leftData = data/2
        rightData = data/2
        self.leftNode = nodeFactory(leftData)
        self.rightNode = nodeFactory(rightData)
