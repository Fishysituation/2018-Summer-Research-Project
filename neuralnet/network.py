import numpy as np


#network class
class network():

    def __init__(self, structure, weights, biases, function):
        #number of nodes in each layer
        self.structure = structure
        #len(structure)-1 lists of dimension strucure[i]
        #list of numpy tensors
        self.weights = weights
        #len(structure)-1 lists of dimension strucure[i+1]
        #list of numpy tensors
        self.biases = biases
        #choose which activation function to use
        self.function = function


    #feed inputs forward through whole network
    def feedForward(self, inputs):
        #assign initial activations to inputNo-D column vector
        activations = np.asarray(inputs).reshape(self.structure[0], 1)
        
        #for each action layer
        for i in range(0, len(self.structure)-1):
            #calculate values of activations applied to weights and biases
            unsquished = (self.weights[i] @ activations) + self.biases[i]
            #parse through the activation function
            activations = self.squish(unsquished)

        return activations


    #return value and index of highest activation value
    def getHighestActivation(self, activations):
        #when finished, return output number and activation
        highest = activations[0]
        index = 0

        for i in range(1, len(activations)):
            if activations[i] > highest:
                highest = activations[i]
                index = i
        
        return index, highest[0]


    #if only one output, return binary value of it
    def binaryOutput(self, activation):
        value = activation[0]
        if value > 0.5:
            return 1
        else:
            return 0 


    #feed vector of calculated vales through chosen activation function
    def squish(self, vector):
        if self.function == "sigmoid":
            return np.apply_along_axis(self.sigmoid, 1, vector)


    def sigmoid(self, value):
        return 1/(1+np.exp(-value))



#return net instance from weights and biases string
#hard coded because I was lazy :(
def initiate(structure, string):
    weights = []
    biases = []

    #first layer
    weights.append(
        np.array([
            [string[0], string[1]],
            [string[2], string[3]]
        ])
    )

    biases.append(
        np.array([
            [string[8]],
            [string[9]]
        ])
    )


    #output layer
    weights.append(
        np.array([
            [string[4], string[5]],
            [string[6], string[7]]
        ])
    )

    biases.append(
        np.array([
            [string[10]],
            [string[11]]
        ])
    )
    

    return network(structure, weights, biases, "sigmoid")



#reads network in from dir, return initialised network instance
def loadIn(pathIn):
    return

    
