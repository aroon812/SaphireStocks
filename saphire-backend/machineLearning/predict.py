from .data import inputsForBackProp
from .neural_network import NeuralNet
from .predictor import prediction_calc
from api.stockUtils import get_past_days
import pandas as pd
import numpy as np
from datetime import datetime


def predictStock(ticker, date):
    NODES_PER_LAYER = [95,2,2,2,1]
    ACTIVATION_FUNCTIONS = [0,1,0,3]
    WEIGHTS_FILE_PATH = './machineLearning/data/Brody.npy'

    network = NeuralNet.NeuralNet(ACTIVATION_FUNCTIONS, NODES_PER_LAYER)
    weights = np.load(WEIGHTS_FILE_PATH,allow_pickle=True)
    network.weights = weights
    inputs1 = inputsForBackProp.getInputs(ticker,date, 20)
    prediction1 = network.calculateOutput(inputs1, single_input=True)
    #print(type(date))
    inputs2 = pd.DataFrame(list(get_past_days(30, datetime.strptime(date, '%Y-%m-%d'), ticker).values()))
    prediction2 = prediction_calc(inputs2)

    return (prediction1, prediction2)