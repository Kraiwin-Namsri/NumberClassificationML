import random
import math
import pygame
from mnist import MNIST

#first and last are input and output nodes, so no w+b apply
nodeStructure = [784,28,10] #28 is pretty random, but chosen because 28 is one dimension of the input
WINDOW_SIZE = WIDTH, HEIGHT = 800,800
class Node():
    nodes = []
    outputNodes = []
    guessValues = []
    def __init__(self, layer, amount):
        self.layer = layer
        self.input = 0
        self.output = 0
        self.positionX = 0
        self.positionY = 0
        if layer != 0:
            # Every node that is not in the first layer has weights
            self.weight = Node.RandomWeights(nodeStructure[layer-1]) #should also maybe have the ascosiated nodes in it as object
        else:
            self.weight = None
        if layer != 0 and (layer != (len(nodeStructure)-1)):
            # Every node has a single bias that is not in the first or last layer.
            self.bias = Node.RandomBiases()
        else:
            self.bias = None
        self.id = amount #number node in layer
        Node.nodes.append(self)
    def Initialize():
        for layer, nodeAmount in enumerate(nodeStructure):
            for amount in range(nodeAmount):
                node = Node(layer, amount)
                if node.layer == (len(nodeStructure)-1): #added later for speed
                    Node.outputNodes.append(node)
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
    def Update(objectIMG):
        Data.currentImage = objectIMG
        rawInputs = objectIMG.pixels
        inputs = []
        for rawInput in rawInputs:
            inputs.append(rawInput/255)
        #put the input in the input nodes.
        for i in range(0, Data.imageSize[0]*Data.imageSize[1]):
            Node.nodes[i].input = inputs[i]
        #update all nodes sequentually
        for node in Node.nodes: #Remember that nodes are correctly sorted
            if node.layer == 0:
                #inputnodes don't have weights nor biases
                node.output = node.input 
            elif node.layer == (len(nodeStructure)-1):
                #Output nodes dont have biases, but have weights
                weightedSum = 0
                for prevNode in Node.nodes:
                    if node.layer == prevNode.layer+1:
                        weightedSum += prevNode.output*node.weight[prevNode.id]
                        node.input = weightedSum
                node.output = Node.SquashingFunction(node.input)
            else:#normal nodes
                weightedSum = 0
                weightedSum += node.bias
                for prevNode in Node.nodes:
                    if node.layer == prevNode.layer+1:
                        weightedSum += prevNode.output*node.weight[prevNode.id]
                        node.input = weightedSum
                node.output = Node.SquashingFunction(node.input)
            #above can be coded in less lines, but now its much more readable
            Node.PercentageGuess()
            Node.CostFunction(objectIMG)
    def PercentageGuess():
        guessValuesBuffer = []
        guessSum = 0
        for node in Node.outputNodes:
            guessSum += node.output
            guessValuesBuffer.append(node.output)
        Node.guessValues = []
        for value in guessValuesBuffer:
            if guessSum != 0:
                Node.guessValues.append(value/guessSum)
    def CostFunction(objectIMG):
        imageCost = []
        for idx, node in enumerate(Node.outputNodes):
            if objectIMG.label == idx:
                imageCost.append((node.output-1)**2) #when its correct
            else:
                imageCost.append((node.output-0)**2) #When its wrong
        Data.BatchCosts.append(imageCost)
class Data:
    imageSize = (28,28)
    image = []
    batchSize = 8 #means 7500 batches with sample size of 60000
    batch = []
    currentBatch = None
    availableBatches = []
    currentImage = None
    BatchCosts = []
    def __init__(self, pixels, label) -> None:
        self.pixels = pixels
        self.label = label
        Data.image.append(self)
    def Initialize():
        #load data
        mndata = MNIST('Dataset/mnist/Samples')
        images, labels = mndata.load_training()
        #Create Objects for all images
        for idx, image in enumerate(images):
            Data(image,labels[idx])
        #Create Random Batches
        imageBuffer = random.sample(Data.image, len(Data.image))
        batch = []
        for image in imageBuffer:
            batch.append(image)
            if len(batch) == Data.batchSize:
                Data.batch.append(batch)
                batch = []
        #select random batch
        Data.availableBatches = [*range(0, len(Data.batch)-1)]
        random.shuffle(Data.availableBatches)
        Data.SelectRandomBatch()
    def SelectRandomBatch():
        Data.BatchCosts = []
        randomIdx = random.randint(0, len(Data.availableBatches)-1)
        Data.currentBatch = Data.availableBatches[random.randint(0, len(Data.availableBatches)-1)]
        Data.availableBatches.pop(randomIdx)
        
class Render:
    global WHITE
    WHITE = (255,255,255)
    global highest
    global GREEN
    GREEN = (0, 255,0)
    def Initialize():
        pygame.display.init()
        global SCREEN
        SCREEN = pygame.display.set_mode(WINDOW_SIZE)
        pygame.font.init()
        global FONT
        global FONT2
        FONT = pygame.font.SysFont('Comic Sans MS', 30)
        FONT2 = pygame.font.SysFont('Comic Sans MS', 15)
    def DrawWindow():
        #draw NN to surface
        neuralNetworkSize = (400, 400)
        neuralNetworkSurface = pygame.Surface(neuralNetworkSize)
        weightsSurface = pygame.Surface(neuralNetworkSize, pygame.SRCALPHA, 32)
        neuronsSurface = pygame.Surface(neuralNetworkSize, pygame.SRCALPHA, 32)
        neuralNetworkPosition = (0,0)
        neuronRadius = 15
        neuronOutputTextPosition = (neuralNetworkSize[0], neuralNetworkPosition[1])
        neuronOutputTextSize = (100, neuralNetworkSize[1])
        neuronOutputTextSurface = pygame.Surface(neuronOutputTextSize)
        for idx, node in enumerate(Node.nodes):
            #Print all neurons
            #color should be represantative of bias
            node.positionX = ((neuralNetworkSize[0])/(len(nodeStructure)+1))*(node.layer+1)
            node.positionY = ((neuralNetworkSize[1])/(nodeStructure[node.layer]+1))*(node.id+1)
            color = (node.output*255,node.output*255,node.output*255)
            pygame.draw.circle(neuronsSurface, color, (node.positionX, node.positionY), neuronRadius)

            if node.layer != 0:
                for idxWeight, weight in enumerate(node.weight):
                    for idxToNode, toNode in enumerate(Node.nodes):
                        if toNode.id == idxWeight and toNode.layer == node.layer -1:
                            oldRange = (3+3)  
                            newRange = (255+0)
                            color = ((((weight + 3) * newRange) / oldRange), (((weight + 3) * newRange) / oldRange), (((weight + 3) * newRange) / oldRange))
                            pygame.draw.line(weightsSurface, color, (node.positionX, node.positionY), (toNode.positionX, toNode.positionY))
            if node.layer == (len(nodeStructure)-1):
                outputText = FONT2.render(str(node.id)+": "+str(round(Node.guessValues[node.id]*100))+"%",False, WHITE)
                neuronOutputTextSurface.blit(outputText, (0, node.positionY))
            #Neurons on top of Weights:
            neuralNetworkSurface.blit(weightsSurface, (0,0))
            neuralNetworkSurface.blit(neuronsSurface, (0,0))
            
        #for data visualization image
        dataSize = (800,800)
        dataPosition = (60,650)
        dataSurface = pygame.Surface(dataSize)

        for imageNumber, image in enumerate(Data.batch[Data.currentBatch]):
            numberSurface = pygame.Surface(Data.imageSize)
            numberSizeMultiplier = 3
            for idx, pixel in enumerate(image.pixels):
                pos = ((idx%Data.imageSize[0]),(idx//Data.imageSize[1]))
                color = (pixel,pixel,pixel)
                numberSurface.fill(color, (pos,(1,1)))
            numberSurface = pygame.transform.scale(numberSurface, (Data.imageSize[0]*numberSizeMultiplier,Data.imageSize[1]*numberSizeMultiplier))
            labelText = FONT.render(" "+str(image.label),False, WHITE)# for the centering :)
            labelPosition = ((imageNumber*Data.imageSize[0]*numberSizeMultiplier)+(Data.imageSize[0]),Data.imageSize[1]*numberSizeMultiplier)
            numberPosition = (imageNumber*Data.imageSize[0]*numberSizeMultiplier,0)
            #To see wich one is inputted into the NN
            inputSurface = pygame.Surface((dataSize[0],10))
            if image == Data.currentImage:
                pygame.draw.rect(inputSurface, GREEN, pygame.Rect(0,0,55,10))
            dataSurface.blit(inputSurface, (labelPosition[0]-10, labelPosition[1]+40))
            dataSurface.blit(labelText, labelPosition)
            dataSurface.blit(numberSurface, numberPosition)
        
        #Draw Costs as text
        costSize = (800,40)
        costPosition = (0,400)
        costSurface = pygame.Surface(costSize)
        sumImages = 0
        #definetly not correct
        buffer = []
        for image in Data.BatchCosts:
            for cost in image:
                buffer.append(cost)
        average = sum(buffer)/len(buffer)
        batchCostText = FONT2.render("BatchCost: "+str(average),False, WHITE)
        costSurface.blit(batchCostText, (0,0))

        #draw all surfaces to the screen
        SCREEN.blit(neuralNetworkSurface, neuralNetworkPosition)
        SCREEN.blit(neuronOutputTextSurface, neuronOutputTextPosition)
        SCREEN.blit(dataSurface, dataPosition)
        SCREEN.blit(costSurface, costPosition)
    def ColorFilter(color): #input is RGB tuple currently pretty shit
        r = color[0]
        g = color[1]
        b = color[2]
        changedColor = ((255/(1+(math.e**(r*0.01)+1))),(255/(1+(math.e**(-g*0.02)+2))),(255/(1+(math.e**(-b*0.03)+3))))
        return changedColor

def Initialize():
    Render.Initialize()
    Node.Initialize()
    Data.Initialize()

Initialize()
run = True
image = 0
while run:
    Node.Update(Data.batch[Data.currentBatch][image])
    Render.DrawWindow()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #update te current image
    image += 1
    if image > len(Data.batch[Data.currentBatch])-1:
        image = 0
        Data.SelectRandomBatch()