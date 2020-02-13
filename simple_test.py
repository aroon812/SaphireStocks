import random
import matrixMult as net
import gradientDescent as gd

data = [ [ i*(j**2) for i in range(10) ] for j in range(10) ] 

weights = [[ [ random.randint(1,10) for i in range(5) ] for j in range(2) ],
             [ [ random.randint(1,10) for i in range(2) ] for j in range(5) ],
             [ [ random.randint(1,10) for i in range(1) ] for j in range(2) ]]

output = net.calculateOutput( [4,4,4], weights, [4,5], 0)
print(output)
print(gd.errorCalc(data[4][5],output[-1][-1][-1]))
gd.gdBackprop(weights, output[0][:2], output[1][:3], net.derivReLU, net.derivReLU, 1,output[0][-1][0] ,output[1][-1][0], gd.errorCalcDeriv, data[4][5])

