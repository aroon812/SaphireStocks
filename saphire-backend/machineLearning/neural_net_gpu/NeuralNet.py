import math
import numpy as np
import random
import activation_functions as af
from numba import jit

weights = [[]]
errorCalc = None
activation_functions = []
last_output = None
last_out_val = None

@jit
def start(activation_funcs, nodes_per_layer):

    #checks gives correct weight info as input
    num_layers = len(nodes_per_layer)
    weights =  [np.random.rand(nodes_per_layer[k],nodes_per_layer[k+1])  for k in range(num_layers-1) ]
    
    #checks activation functions
    if len(activation_funcs) == len(weights):
        activation_functions = activation_funcs
    else:
        print("invalid action functions")
        print(activation_funcs, weights)

    #default is error squared
    errorCalc = sqErrorCalc


#given an input to the neuralnet calculates the output
@jit
def calculateOutput( input, rando = None):
    b=len(weights);
    listToBeReturned=[]
    other=[]
    for a in range(0,b):
        listToBeReturned.append(input);
        if(a == 0):
            other.append(input)
        try:
            output= np.dot(weights[a].T, input)
            other.append(output)
        except ValueError: 
            print("Matrices were invalid dimensions or...")
        active= activation_functions[a]
        input = af.func(active,output,rando = rando)

    listToBeReturned.append(input)
    last_output = [listToBeReturned, other]
    last_out_val = other[-1][-1] 
    return last_output

#determines the change of weights for a specific calculation
@jit
def gdBackprop( learnRate, target):
    numLayers = len(weights)
    deltaWeights = [None]*numLayers
    #seperates the last network output to the various components
    pre_nodeValues = last_output[0][:-1]
    post_nodeValues = last_output[1][:-1]
    pre_output = last_output[0][-1][0]
    output = last_output[1][-1][0]
    
    #calculates derivative for final output 
    cost_derivative = af.func(activation_functions[numLayers-1],[pre_output],deriv=True)
    tempPartials = [np.dot(cost_derivative , errorCalc(target, output, deriv= True))]
    for i in range(numLayers):
        layer = -i-1
        #gets the partials for the nodes 
        #gets the weight changes
        deltaWeights[layer]  = -1 * learnRate * layerWeightPartials(post_nodeValues[layer], tempPartials)

        #calculates the partials for the node inputs for the next iteration
        if(i != numLayers-1):
            #for hidden layers only
            tempPartials = nodeDerivatives(pre_nodeValues[layer], weights[layer], activation_functions[i], tempPartials)
    #updates weights
    weights =[weights[i] + deltaWeights[i] for i in range(numLayers)]
    return deltaWeights

#changes the weights for a given input delta weights
@jit
def changeWeights( newWeights):
    weights = newWeights

#helper methods

#helper methods for gradient descent
#gets the partial derivatives dE/dw_ij for an individual layers weights
@jit
def layerWeightPartials( inputVals, outputDerivatives):

    rows = len(inputVals)
    cols = len(outputDerivatives)
    weightPartials = np.zeros((rows,cols))
    # print(inputVals)
    # print(outputDerivatives)
    for i in range(rows):
        for j in range(cols):
            weightPartials[i][j]  = inputVals[i] * outputDerivatives[j]
    
    return weightPartials

#gets the partial derivatives dE/dn_i for an individual layers nodes
@jit
def nodeDerivatives( node_values, output_weights, selector, output_derivatives):
    numNodes = len(node_values)
    nodeParitals = np.zeros(numNodes)

    for i in range(numNodes):
        node_input = [node_values[i]]
        activation_deriv = af.func(selector, node_input, deriv = True)[0]
        nodeParitals[i] = activation_deriv * np.dot(output_weights[i], output_derivatives)

    return nodeParitals

@jit
def backProp( inputs, targets, learnRate = 1, iterations=1000):
    if len(targets) != len(inputs):
        print("invalid size combination for inputs and outputs")
    error = 0
    output = [0]*len(targets)
    for k in range(iterations):
        error = 0
        for i in range(len(inputs)):
            calculateOutput(inputs[i])
            gdBackprop(learnRate, targets[i])
            error = error + sqErrorCalc(targets[i],last_out_val)/16
            output[i] = last_out_val
        if k == 0:
            print("start: ", error)
    print("end: ", error)
    print(targets)
    print(output)


@jit
def sqErrorCalc(target, output, deriv = False):
    if deriv:
        return output - target
    return float(((target - output)**2)/2) 

x = np.array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
y = np.array([[0, 1, 1, 0]])


start([7,7],[3,4,1])
backProp(x,y[0],1,10000)






