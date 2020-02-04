import math;
import numpy;
class Neural Network:
    def calculateOutput(activationFunction, matrix, input, rando):
        b=len(matrix);
        listToBeReturned=[][];
        for a in range(0,b):
            listToBeReturned.append(input);
            try:
                output= matrixMultiplication(matrix[a], input);
            except ValueError: 
                print("Matrices were invalid dimensions or...");
            active= activationFunction[a];
            if(active==1):
                input=activationArcTan(output)
            else if(active==2):
                input=activationELU(output)
            else if(active==3):
                input=activationIdentity(output);
            else if(active==4):
                input=activationLeakyReLU(output);
            else if(active==5):
                input=activationRandomReLU(output, rando);
            else if(active==6):
                input=activationReLU(output);
            else if(active==7):
                input=activationSigmoid(output);
            else if(active==8):
                input=activationSoftPlus(output);
            else if(active==9):
                input=activationStep(output);
            else:
                input=activationTanH(output);
        listToBeReturned.append(input);
        return listToBeReturned;



    def matrixMultiplication(weights, input):
        outputSize= len(weights[0]);
        other= len(weights);
        lenOfInput=len(input);
        output=[];
        bbool=True;
        for alpha in range(0, other):
            if(len(weights[alpha])!=outputSize):
                print(weights[alpha])
                bbool=False
        if(lenOfInput==other and bbool):
            for a in range(0,outputSize):
                sum=0;
                for b in range(0, other):
                    sum+=input[b]*weights[b][a];
                output.append(sum);
            return output;
        else:
            if(bbool):
                raise ValueError("Dimensions are incompatible");
            else:
                raise ValueError("Weights are not all same length");
    def activationSigmoid(input):
        for a in range(0,len(input)):
            z=input[a];
            z=(-1)*z;
            input[a]= 1/(1+math.exp(z));
        return input;
    def activationTanH(input):
        for a in range(0,len(input)):
            z=input[a];
            input[a]=math.tanh(z);
        return input;
    def activationReLU(input):
        for a in range(0,len(input)):
            z=input[a];
            if(z<0):
                input[a]=0;
        return input;
    def activationLeakyReLU(input):
        b=0.01;
        for a in range(0,len(input)):
            z=input[a];
            if(z<0):
                input[a]=z*b;
        return input;
    def activationRandomReLU(input,b):
        for a in range(0,len(input)):
            z=input[a];
            if(z<0):
                input[a]=z*b;
        return input;
    def activationStep(input):
        for a in range(0,len(input)):
            z=input[a];
            if(z<0):
                input[a]=0;
            else:
                input[a]=1;
        return input;
    def activationArcTan(input):
        for a in range(0,len(input)):
            input[a]=numpy.arctan(input[a]);
        return input;
    def activationSoftPlus(input):
        for a in range(0,len(input)):
            z=input[a];
            b=math.log(1+math.exp(z));
            input[a]=b;
        return input;
    def activationELU(input,b):
        for a in range(0,len(input)):
            z=input[a];
            if(z<0):
                q=b*(math.exp(z)-1);
                input[a]=q;
        return input;
    def activationIdentity(input):
        return input;