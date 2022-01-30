from audioop import bias
import enum
import random
import numpy as np
import math
import pygame
#first and last are input and output nodes, so no w+b apply
nodeStructure = [6,5, 1]

class Node():
    nodes = []
    def __init__(self, layer, amount):
        self.layer = layer
        self.input = 0
        self.output = 0
        if layer != 0 and (layer != len(nodeStructure)-1):
            self.weight = Node.RandomWeights(nodeStructure[layer-1])
            self.bias = Node.RandomWeights(nodeStructure[layer-1])
        else:
            self.weight = None
        Node.nodes.append(self)
    def RandomWeights(amountWeights):
        weights = []
        for i in range(amountWeights):
            weights.append(Node.RandomFunction())
        return weights
    def RandomBiases(amountBiases):
        biases = []
        for i in range(amountBiases):
            biases.append(Node.RandomFunction())
        return biases
    def RandomFunction():
        #should be normal distribution
        return random.uniform(-3,3)
    def SquashingFunction(value):
        return 1/(1+(math.e**-value))
    def Update(inputs):
        for idx, node in enumerate(Node.nodes):
            if node.layer == 0:
                node.input = inputs[idx]
            else:
                sum = 0
                for idx, weight in enumerate(node.weight):
                    idx

def Initialize():
    #create every node with weights and biases
    for layer, nodeAmount in enumerate(nodeStructure):
        for amount in range(nodeAmount):
            Node(layer, amount)

Initialize()