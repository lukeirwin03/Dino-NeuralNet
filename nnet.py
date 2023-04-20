import numpy as np
import scipy.special
import random
from var import *

class Nnet():

    def __init__(self, numInput, numHidden, numOutput):
        self.numInput = numInput
        self.numHidden = numHidden
        self.numOutput = numOutput
        self.weightInputHidden = np.random.uniform(-0.5, 0.5, size=(self.numHidden, self.numInput))
        self.weightHiddenOutput = np.random.uniform(-0.5, 0.5, size=(self.numOutput, self.numHidden))
        self.activationFunction = lambda x: scipy.special.expit(x)

    def getOutputs(self, inputs):
        inputs = np.array(inputs, ndmin=2).T
        hiddenInputs = np.dot(self.weightInputHidden, inputs)
        hiddenOutputs = self.activationFunction(hiddenInputs)
        finalInputs = np.dot(self.weightHiddenOutput, hiddenOutputs)
        finalOutputs = self.activationFunction(finalInputs)

        return finalOutputs
    
    def getMaxValue(self, inputs):
        outputs = self.getOutputs(inputs)
        return np.max(outputs)
    
    def modifyWeights(self):
        Nnet.modifyArray(self.weightInputHidden)
        Nnet.modifyArray(self.weightHiddenOutput)

    def createMixedWeights(self, net1, net2):
        self.weightInputHidden = Nnet.getMixFromArrays(net1.weightInputHidden, net2.weightInputHidden)
        self.weightHiddenOutput = Nnet.getMixFromArrays(net1.weightHiddenOutput, net2.weightHiddenOutput)

    def modifyArray(a):
        for val in np.nditer(a, op_flags=['readwrite']):
            if random.random() < MUTATION_WEIGHT_MODIFY_CHANCE:
                val[...] = np.random.random_sample() - 0.5
        
    def getMixFromArrays(arr1, arr2):
        totalEntries = arr1.size
        rows = arr1.shape[0]
        cols = arr1.shape[1]

        numToTake = totalEntries - int(totalEntries * MUTATION_ARRAY_MIX_PERC)
        index = np.random.choice(np.arange(totalEntries), numToTake, replace=False)

        res = np.random.rand(rows, cols)

        for row in range(0, rows):
            for col in range(0, cols):
                i = row * cols + col
                if i in index:
                    res[row][col] = arr1[row][col]
                else:
                    res[row][col] = arr2[row][col]
        
        return res
