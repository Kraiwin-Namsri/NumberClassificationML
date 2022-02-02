import random
from turtle import screensize
import numpy as np
import math
import pygame
from pyparsing import White
#first and last are input and output nodes, so no w+b apply
nodeStructure = [576,24,10]
WINDOW_SIZE = WIDTH, HEIGHT = 1600,1200
class Node():
    nodes = []
    def __init__(self, layer, amount):
        self.layer = layer
        self.input = 0
        self.output = 0
        self.positionX = None
        self.positionY = None
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
        neuralNetworkSize = (400, 400)
        neuralNetworkSurface = pygame.Surface(neuralNetworkSize)
        neuralNetworkPosition = (0,0)
        neuronRadius = 5
        
        for idx, node in enumerate(Node.nodes):
            #Print all neurons
            #color should be represantative of bias
            node.positionX = ((neuralNetworkSize[0])/(len(nodeStructure)+1))*(node.layer+1)
            node.positionY = ((neuralNetworkSize[1])/(nodeStructure[node.layer]+1))*(node.id+1)
            
            pygame.draw.circle(neuralNetworkSurface, WHITE, (node.positionX, node.positionY), neuronRadius)
            #print all links
            #color should be representative of weight
        for idx, node in enumerate(Node.nodes):
            for idx, toNode in enumerate(Node.nodes):
                if toNode.layer == node.layer+1:
                    pygame.draw.line(neuralNetworkSurface, WHITE, (node.positionX, node.positionY), (toNode.positionX, toNode.positionY))
                    
            


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