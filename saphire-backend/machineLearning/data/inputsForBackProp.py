import pandas as pd
import numpy as np
from api.models import StockChange, Company, Stock
from progressbar import ProgressBar
from datetime import timedelta, datetime

def getInputs(tic, date, days): 
    end_date = datetime.strptime(date, '%Y-%m-%d')
    start_date = end_date - timedelta(days=days)
    company = Company.objects.get(symbol=tic)
    regStocks = Stock.objects.filter(company=company, date__range=[start_date, end_date])
    print("length: " + str(len(regStocks)))
    output=[]
    for regStock in regStocks:
        stock = StockChange.objects.get(stock=regStock)

        output.append(float(stock.low))
        output.append(float(stock.high))
        output.append(float(stock.avg))
        output.append(float(stock.vol))
        output.append(float(stock.close))
        output.append(float(stock.open))
        output.append(float(stock.range))
        output.append(float(stock.ema_12_day))
        output.append(float(stock.ema_26_day))
        output.append(float(stock.vol_ema))
        output.append(float(stock.single_day_change))
        output.append(float(stock.day_to_day_change))
        output.append(float(stock.high_52_day))
        output.append(float(stock.high_52_week))
        output.append(float(stock.low_52_day))
        output.append(float(stock.low_52_week))
        output.append(float(stock.avg_52_week))
        output.append(float(stock.stdev_52_day))
        output.append(float(stock.stdev_52_week))
    return np.array(output)
    
#given a set of tickers it returns two dictionaries one mapping 
#a stock to its input vectors and the other mapping a stock to 
#its ouput values
def inputsForBackProp(tics):
    inputters=[]
    outputters=[]
    for tic in [tics]:
        #gets the dates and the assosiated close values
        output_values = pd.read_csv('data/training/' + tic + '.csv')
        #creates an array of input vectors for a given stock and the training days
        input_values = [0]*len(output_values.index)
        data = pd.read_csv('data/normalized_data/' + tic + '.csv')
        data = data.set_index('date')
        i = 0
        for date in output_values.date:
            input = getInputs(tic,date,data)
            #catches error if not enough previous days
            if type(input) ==type(-1):
                output_values = output_values[output_values.date != date]
                input_values = input_values[:-1]
            else:
                input_values[i] = input
                i = i + 1
            

        inputters.append(input_values)
        outputters.append(output_values['dayToDay'].to_numpy())
    #map tics to their respective lists of inputs and outputs
    input_dict=dict(zip([tics], inputters))
    output_dict=dict(zip([tics],outputters))
    #return list of both dicts
    return [input_dict, output_dict]
    
#given a set of tickers it returns two dictionaries one mapping 
#a stock to its input vectors and the other mapping a stock to 
#its ouput values
def inputsForTesting(tics):
    inputters=[]
    outputters=[]
    for tic in [tics]:
        #gets the dates and the assosiated close values
        output_values = pd.read_csv('data/testing/' + tic + '.csv')
        #creates an array of input vectors for a given stock and the training days
        input_values = [0]*len(output_values.index)
        data = pd.read_csv('data/normalized_data/' + tic + '.csv')
        data = data.set_index('date')
        i = 0
        for date in output_values.date:
            input = getInputs(tic,date,data)
            #catches error if not enough previous days
            if type(input) ==type(-1):
                output_values = output_values[output_values.date != date]
                input_values = input_values[:-1]
            else:
                input_values[i] = input
                i = i + 1
            

        inputters.append(input_values)
        outputters.append(output_values['dayToDay'].to_numpy())
    #map tics to their respective lists of inputs and outputs
    input_dict=dict(zip([tics], inputters))
    output_dict=dict(zip([tics],outputters))
    #return list of both dicts
    return [input_dict, output_dict]