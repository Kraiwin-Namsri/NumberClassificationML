import random
from turtle import screensize
import numpy as np
import math
import pygame
from pyparsing import White
#first and last are input and output nodes, so no w+b apply
nodeStructure = [30,20,50]
WINDOW_SIZE = WIDTH, HEIGHT = 800,800
class Node():
    nodes = []
    def __init__(self, layer, amount):
        self.layer = layer
        self.input = 0
        self.output = 0
        if layer != 0 and (layer != len(nodeStructure)-1):
            #amount of weight needs to be the same amount as in previous layer.
            self.weight = Node.RandomWeights(nodeStructure[layer-1])
            # Every node has a single bias.
            self.bias = Node.RandomBiases()
        else:
            self.weight = None
            self.bias = None
        self.id = amount
        Node.nodes.append(self)
    def RandomWeights(amountWeights):
        weights = []
        for i in range(amountWeights):
            weights.append(Node.RandomFunction())
        return weights
    def RandomBiases():
        return Node.RandomFunction()
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
class Render:
    global WHITE
    WHITE = (255,255,255)
    def DrawWindow():
        #draw NN to surface
        neuralNetworkSize = (800, 800)
        neuralNetworkSurface = pygame.Surface(neuralNetworkSize)
        neuralNetworkPosition = (0,0)
        neuronRadius = 10
        neuronWidthOffset = (neuralNetworkSize[0])/(len(nodeStructure)+1)
        for idx, node in enumerate(Node.nodes):
            neuronHeightOffset = (neuralNetworkSize[1])/(nodeStructure[node.layer]+1)
            pygame.draw.circle(neuralNetworkSurface, WHITE, ((neuronWidthOffset*(node.layer+1)), (neuronHeightOffset*(node.id+1))), neuronRadius)
            print(node.layer)
        
            


        #draw all surfaces to the screen
        SCREEN.blit(neuralNetworkSurface, neuralNetworkPosition)
        

def Initialize():
    #create every node with weights and biases
    for layer, nodeAmount in enumerate(nodeStructure):
        for amount in range(nodeAmount):
            Node(layer, amount)
    pygame.display.init()
    global SCREEN
    SCREEN = pygame.display.set_mode(WINDOW_SIZE)

Initialize()

run = True
while run:
    Render.DrawWindow()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False