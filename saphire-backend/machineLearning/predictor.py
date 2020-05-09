import pandas as pd
import numpy as np
import os
from .neural_network import NeuralNet as nn

RAW_DATA_FOLDER = 'data/historical_stock_data/'
WEIGHTS_FILE_PATH = './machineLearning/data/end_weights.npy'

def getInputs(date, inputData): 
    listOfDates= list(inputData.index)
    listOfNums=[x for x in range(0,len(listOfDates))]
    datesToNums= dict(zip(listOfDates, listOfNums))
    new_dict = dict([(value, key) for key, value in datesToNums.items()]) 
    try:
        beginningIndex= datesToNums[date]
    except:
        return -1
    endIndex=beginningIndex-20
    if(endIndex<0):
        return -1
    relevantDates=[]
    for i in range(endIndex, beginningIndex):
        relevantDates.append(new_dict[i])
    output=[]
    for i in relevantDates[-20:]:
        output.append(float(inputData['close'][i]))
        if i == relevantDates[-1]:
            output.append(float(inputData['range'][i]))
            output.append(float(inputData['singleDay'][i]))
            output.append(float(inputData['dayToDay'][i]))
            output.append(float(inputData['low'][i]))
            output.append(float(inputData['high'][i]))
            output.append(float(inputData['average'][i]))
            output.append(float(inputData['open'][i]))
            if inputData['dayToDay'][i] > 0:
                output.append(1)
            else:
                output.append(0)
            if inputData['twelveDay'][i]- inputData['twelveDay'][relevantDates[-2]] > 0:
                output.append(1)
            else:
                output.append(0)
            if inputData['twentySixDay'][i]- inputData['twentySixDay'][relevantDates[-2]] > 0:
                output.append(1)
            else:
                output.append(0)
            output.append(float(inputData['volume'][i] - inputData['volume'][relevantDates[-2]]))
            output.append(float(inputData['twelveDay'][i]- inputData['twelveDay'][relevantDates[-2]]))
            output.append(float(inputData['twentySixDay'][i]- inputData['twentySixDay'][relevantDates[-2]]))
            output.append(float(inputData['volumeEMA'][i]))
            output.append(float(inputData['fiftyTwoDayHigh'][i]))
            output.append(float(inputData['fiftyTwoWeekHigh'][i]))
            output.append(float(inputData['fiftyTwoDayLow'][i]))
            output.append(float(inputData['fiftyTwoWeekLow'][i]))
            output.append(float(inputData['fiftyTwoWeekAverage'][i]))
            output.append(float(inputData['fiftyTwoDayStandDev'][i]))
            output.append(float(inputData['fiftyTwoWeekStandDev'][i]))
    return np.array(output)
def percentChange(low,high, value):
    if high-low!=0 :
        div = (value - low)/(high - low)
        """ if div < 0:
            print("high: ", high, " low: ", low, " value", value)
            raise Exception """
        return 2*div-1
    else:
        return .5
def transform(vals):
    v=[[]]
    alpha=len(vals[0])-1
    while(alpha>0):
        v.append([])
        alpha-=1
    for k in range(0,len(vals[0])):
        for j in range(0,len(vals)):
            v[k].append(vals[j][k])
    return v
def normalize(data):
    low= [0]*len(data['low'])
    high= [0]*len(data['low'])
    average= [0]*len(data['low'])
    volume= [0]*len(data['low'])
    close= [0]*len(data['low'])
    openn= [0]*len(data['low'])
    rangee= [0]*len(data['low'])
    twelveDay= [0]*len(data['low'])
    twentySixDay= [0]*len(data['low'])
    volumeEMA= [0]*len(data['low'])
    singleDay= [0]*len(data['low'])
    dayToDay= [0]*len(data['low'])
    fiftyTwoDayHigh= [0]*len(data['low'])
    fiftyTwoWeekHigh= [0]*len(data['low'])
    fiftyTwoDayLow= [0]*len(data['low'])
    fiftyTwoWeekLow= [0]*len(data['low'])
    fiftyTwoWeekAverage= [0]*len(data['low'])
    fiftyTwoDayStandDev= [0]*len(data['low'])
    fiftyTwoWeekStandDev= [0]*len(data['low'])
    for i in range(len(data['high'])):
        if(i <= 10):
            lowIndex = 0
        else:
            lowIndex = i-10

        priceLow = data['low'][lowIndex:i+1].min()
        priceHigh = data['high'][lowIndex:i+1].max()
        volLow = data['vol'][lowIndex:i+1].min()
        volHigh = data['vol'][lowIndex:i+1].max()
        volemaLow = data['vol_ema'][lowIndex:i+1].min()
        volemaHigh = data['vol_ema'][lowIndex:i+1].max()
        rangeLow = data['range'][lowIndex:i+1].min()
        rangeHigh = data['range'][lowIndex:i+1].max()
        sdayLow = data['single_day_change'][lowIndex:i+1].min()
        sdayHigh = data['single_day_change'][lowIndex:i+1].max()
        ddayLow = data['day_to_day_change'][lowIndex:i+1].min()
        ddayHigh = data['day_to_day_change'][lowIndex:i+1].max()
        deviationLow = data['stdev_52_week'][lowIndex:i+1].min()
        deviationHigh = data['stdev_52_week'][lowIndex:i+1].max()
        ddeviationLow = data['stdev_52_day'][lowIndex:i+1].min()
        ddeviationHigh = data['stdev_52_day'][lowIndex:i+1].max()
        pwLow = data['low_52_week'][lowIndex:i+1].min()
        pwHigh = data['high_52_week'][lowIndex:i+1].max()
        emaLow = data['ema_26_day'][lowIndex:i+1].min()
        emaHigh = data['ema_26_day'][lowIndex:i+1].max()

        low[i]=percentChange(priceLow,priceHigh, data['low'][i])
        high[i]=percentChange(priceLow,priceHigh, data['high'][i])
        average[i]=percentChange(priceLow,priceHigh, data['avg'][i])
        close[i]=percentChange(priceLow,priceHigh, data['close'][i])
        openn[i]=percentChange(priceLow,priceHigh, data['open'][i])
        rangee[i]=percentChange(rangeLow,rangeHigh, data['range'][i])
        twelveDay[i]=percentChange(priceLow,priceHigh, data['ema_12_day'][i])
        twentySixDay[i]=percentChange(priceLow,priceHigh, data['ema_26_day'][i])
        volume[i]=percentChange(volLow,volHigh,data['vol'][i])
        volumeEMA[i]=percentChange(volemaLow,volemaHigh,data['vol_ema'][i])
        singleDay[i]=percentChange(sdayLow,sdayHigh, data['single_day_change'][i])
        dayToDay[i]=percentChange(ddayLow,ddayHigh, data['day_to_day_change'][i])
        fiftyTwoDayHigh[i]=percentChange(pwLow,pwHigh, data['high_52_day'][i])
        fiftyTwoWeekHigh[i]=percentChange(pwLow,pwHigh, data['high_52_week'][i])
        fiftyTwoDayLow[i]=percentChange(pwLow,pwHigh, data['low_52_day'][i])
        fiftyTwoWeekLow[i]=percentChange(pwLow,pwHigh, data['low_52_week'][i])
        fiftyTwoWeekAverage[i]=percentChange(pwLow,pwHigh, data['avg_52_week'][i])
        fiftyTwoDayStandDev[i]=percentChange(ddeviationLow,ddeviationHigh, data['stdev_52_day'][i])
        fiftyTwoWeekStandDev[i]=percentChange(deviationLow,deviationHigh, data['stdev_52_week'][i])
        """ if low[i] < 0:
            print("high: ", priceHigh, " low: ", priceLow, " value", data['low'][i], " output: ", low[i])
            raise Exception """
    listOfDates= data['date']
    listOfVols= data['vol_avg_52_week']
    listOfAverages= data['avg_52_day']
    vals= [low, high, average, volume, close, openn, rangee, twelveDay, twentySixDay,volumeEMA, singleDay, dayToDay,fiftyTwoDayHigh,fiftyTwoWeekHigh,fiftyTwoDayLow,fiftyTwoWeekLow,fiftyTwoWeekAverage,fiftyTwoDayStandDev,fiftyTwoWeekStandDev]  
    v=transform(vals)
    rows=listOfDates
    cols=["low", "high", "average", "volume", "close", "open", "range", "twelveDay", "twentySixDay","volumeEMA", "singleDay", "dayToDay","fiftyTwoDayHigh","fiftyTwoWeekHigh","fiftyTwoDayLow","fiftyTwoWeekLow","fiftyTwoWeekAverage","fiftyTwoDayStandDev","fiftyTwoWeekStandDev"] 
    dataframe=pd.DataFrame(data=v, index=rows, columns=cols)
    return dataframe

def prediction_calc(data, tic=None):
    print(os.getcwd())
    if data is None:
        data = pd.read_csv(RAW_DATA_FOLDER + tic + '.csv').tail(30)
    data.index = range(len(data))
    data = normalize(data)
    date = data.index[-1]
    print(date)
    inputs = getInputs(date,data)
    weights = np.load(WEIGHTS_FILE_PATH,allow_pickle=True)
    
    network = nn.NeuralNet([0,0,7],[41,100,50,1])
    network.weights = weights
    prediction = network.calculateOutput(inputs,single_input=True)
    if prediction > .5:
        confidence = ((prediction-.5)/.4)*100
        return (1,confidence)
    else:
        confidence = np.sqrt((.5-prediction)/.4)*100
        return (0,confidence)
    

#print(prediction_calc('A'))