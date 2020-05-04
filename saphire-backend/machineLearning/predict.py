from .data import inputsForBackProp
from .neural_network import NeuralNet

def predictStock(ticker, date):
    NODES_PER_LAYER = [380,100,50,50,20,1]
    ACTIVATION_FUNCTIONS = [7,7,7,4,3]
    network = NeuralNet.NeuralNet(ACTIVATION_FUNCTIONS, NODES_PER_LAYER)
    inputs = inputsForBackProp.getInputs(ticker,date, 20)
    return network.calculateOutput(inputs)