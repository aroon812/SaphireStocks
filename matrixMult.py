import math;
import numpy;
class NeuralNetwork:
    def calculateOutput(self, activationFunction, matrix, input, rando):
        b=len(matrix);
        listToBeReturned=[]
        other=[]
        for a in range(0,b):
            listToBeReturned.append(input);
            try:
                output= matrixMultiplication(matrix[a], input)
                other.append(output)
            except ValueError: 
                print("Matrices were invalid dimensions or...")
            active= activationFunction[a]
            if(active==1):
                input=activationArcTan(output)
            elif(active==2):
                input=activationELU(output)
            elif(active==3):
                input=activationIdentity(output)
            elif(active==4):
                input=activationLeakyReLU(output)
            elif(active==5):
                input=activationRandomReLU(output, rando)
            elif(active==6):
                input=activationReLU(output)
            elif(active==7):
                input=activationSigmoid(output)
            elif(active==8):
                input=activationSoftPlus(output)
            elif(active==9):
                input=activationStep(output)
            else:
                input=activationTanH(output)
        listToBeReturned.append(input)
        return [listToBeReturned, other] 



    def matrixMultiplication(self, weights, input):
        outputSize= len(weights[0])
        other= len(weights)
        lenOfInput=len(input)
        output=[]
        bbool=True
        for alpha in range(0, other):
            if(len(weights[alpha])!=outputSize):
                print(weights[alpha])
                bbool=False
        if(lenOfInput==other and bbool):
            for a in range(0,outputSize):
                sum=0
                for b in range(0, other):
                    sum+=input[b]*weights[b][a]
                output.append(sum)
            return output
        else:
            if(bbool):
                raise ValueError("Dimensions are incompatible")
            else:
                raise ValueError("Weights are not all same length")
    def activationSigmoid(self,input):
        for a in range(0,len(input)):
            z=input[a]
            z=(-1)*z
            input[a]= 1/(1+math.exp(z))
        return input
    def derivSigmoid(self,input):
        z=activationSigmoid(self,input)
        for a in range(0,len(input)):
            input[a]=z[a]*(1-z[a])
        return input
    def activationTanH(self,input):
        for a in range(0,len(input)):
            z=input[a]
            input[a]=math.tanh(z)
        return input
    def derivTanH(self, input):
        z=activationTanH(self,input)
        for a in range(0,len(input)):
            input[a]=1-z[a]*z[a]
        return input
    def activationReLU(self,input):
        for a in range(0,len(input)):
            z=input[a]
            if(z<0):
                input[a]=0
        return input
    def derivReLU(self, input):
        for a in range(0,len(input)):
            z=input[a]
            if(z<0):
                input[a]=0
            else:
                input[a]=1
        return input
    def activationLeakyReLU(self, input):
        b=0.01
        for a in range(0,len(input)):
            z=input[a]
            if(z<0):
                input[a]=z*b
        return input
    def derivLeakyReLU(self, input):
        for a in range(0, len(input)):
            z=input[a]
            if(z<0):
                input[a]=0.01
            else:
                input[a]=1
        return input
    def activationRandomReLU(self, input,b):
        for a in range(0,len(input)):
            z=input[a]
            if(z<0):
                input[a]=z*b
        return input
    def derivRandomReLU(self, input, b):
        for a in range(0,len(input)):
            z=input[a]
            if(z<0):
                input[a]=b
            else:
                input[a]=1
        return input
    def activationStep(self, input):
        for a in range(0,len(input)):
            z=input[a]
            if(z<0):
                input[a]=0
            else:
                input[a]=1
        return input
    def derivStep(self, input):
        for a in range(0,len(input)):
            if(input[a]!=0):
                input[a]=0
            else:
                raise ValueError("Not differentiable")
        return input
    def activationArcTan(self, input):
        for a in range(0,len(input)):
            input[a]=numpy.arctan(input[a])
        return input
    def derivArcTan(self,input):
        for a in range(0,len(input)):
            z=input[a]*input[a]+1
            input[a]=1/z
        return input
    def activationSoftPlus(self, input):
        for a in range(0,len(input)):
            z=input[a]
            b=math.log(1+math.exp(z))
            input[a]=b
        return input
    def derivSoftPlus(self,input):
        return activationSigmoid(self,input)
    def activationELU(self, input, b):
        for a in range(0,len(input)):
            z=input[a]
            if(z<0):
                q=b*(math.exp(z)-1)
                input[a]=q
        return input
    def derivELU(self, input, b):
        z=activationELU(self, input, b)
        for a in range(0,len(input)):
            input[a]=z[a]+b
        return input
    def activationIdentity(self, input):
        return input
    def derivIdentity(self, input):
        for a in range(0,len(input)):
            input[a]=1
        return input