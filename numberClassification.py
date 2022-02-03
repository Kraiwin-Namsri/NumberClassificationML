import random
import math
import pygame
import csv

#first and last are input and output nodes, so no w+b apply
nodeStructure = [10,24,10]
WINDOW_SIZE = WIDTH, HEIGHT = 1600,1200
class Node():
    nodes = []
    def __init__(self, layer, amount):
        self.layer = layer
        self.input = 0
        self.output = 0
        self.positionX = 0
        self.positionY = 0
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
    def Initialize():
        for layer, nodeAmount in enumerate(nodeStructure):
            for amount in range(nodeAmount):
                Node(layer, amount)
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
class Data:
    train = None
    test = None
    def Initialize():
        #first value is label
        with open("Dataset/mnist/csv/mnist_train.csv", newline='') as f:
            reader = csv.reader(f)
            Data.train = list(reader)
        with open("Dataset/mnist/csv/mnist_test.csv", newline='') as f:
            reader = csv.reader(f)
            Data.test = list(reader)
class Render:
    global WHITE
    WHITE = (255,255,255)
    def Initialize():
        pygame.display.init()
        global SCREEN
        SCREEN = pygame.display.set_mode(WINDOW_SIZE)
        pygame.font.init()
        global FONT
        FONT = pygame.font.SysFont('Comic Sans MS', 30)
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
        
        #for data visualization
        dataSize = (100,100)
        dataSurface = pygame.Surface(dataSize)
        dataPosition = (400,400)
        labelText = FONT.render(Data.train[0][0],False, WHITE)
        dataSurface.blit(labelText, (50,50))
        #draw all surfaces to the screen
        SCREEN.blit(neuralNetworkSurface, neuralNetworkPosition)
        SCREEN.blit(dataSurface, dataPosition)


def Initialize():
    Render.Initialize()
    Node.Initialize()
    Data.Initialize()


Initialize()
run = True
while run:
    Render.DrawWindow()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False