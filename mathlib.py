#!/usr/bin/env python

import numpy as np
import sympy as sp
import math
import copy
"""This library is filled with helper functions, from generating the encessary
matrix to interpreting this same matrix. If you want to see how these work, feel
free to execute this script to execute/see each command in context"""

def generateMatrix(size):
    """This function generates a 20x20 matrix, for use with RREF and accurate
    data interpolation"""
    returnedArray=[]
    for i in range(-1 * size,0):
        constructedArray=[]
        constructedArray.append(1)
        for j in range(1,size):
            constructedArray.append(i**j)#Raise i to the jth power, in order to satisfy the polinomial at position len(array)+i in the array
        returnedArray.append(constructedArray)
    return returnedArray

def addAverages(matrix,averages):
    """This function simply adds each average value to the end of our 20x20 matrix"""
    neo=copy.deepcopy(matrix)
    for row in range(len(neo)):
        neo[row].append(averages[row])

    return neo

def convertMatrixAndRREF(listMatrix):
    """This function is designed to take a 2d array from python and convert it to
    a numpy matrix in order to allow us to use optimized algorithms in sympy"""
    return sp.Matrix(np.matrix(listMatrix)).rref()



def generateAverageDeviations(twoDArray):
    """This function is going to return THREE average matricies. Make sure you catch
    them in the form \"lowerdiv,average,upperdiv = generateAverageDeviations(averagematrix)\"
    You will need to run each data set with the lower, average, and upper respectivly in order
    to get an accurate range for your distrobution"""

    twoTail=.1729
    sampleSize=math.sqrt(19)


    lowerMatrix,averageMatrix,upperMatrix=[],[],[]
    for year in twoDArray:
        average=0
        standardDeviation=0
        for publishedNum in year:
            average+=publishedNum
        average /= len(year)
        for publishedNum in year:
            standardDeviation+=(average-publishedNum)**2
        standardDeviation /= len(year)
        averageMatrix.append(average)
        lowerMatrix.append(average-(twoTail*(standardDeviation/sampleSize)))
        upperMatrix.append(average+(twoTail*(standardDeviation/sampleSize)))
    return lowerMatrix,averageMatrix,upperMatrix






def rowReduce(matrix):
    """This function will reduce the rows without switching. It's fairly expensive
    computationally. To reduce, we will reduce the rows ith term to 1(where i is
    a column that will contain a single 1 and all 0's) to 1 by dividing the entire
    row by the same ith term.

    From there, we will add the ith term's row to all other rows beneath it.
    This is repeated until every row is reduced to 1.

    This function currently doesn't work."""
    for row in range(len(matrix)):
        if(matrix[row] is not 1):
            divisor=matrix[row][row]
            for i in range(row,len(matrix[row])):
                matrix[row][i]=matrix[row][i]/divisor
        #Now that we have this in row eschlon form, we can reduce the rest of the rows
        if row is not len(matrix):
            for otherRows in range(len(matrix)):
                currentRow=matrix[row]
                for cell in range(row,len(matrix[row])):
                    currentRow[cell]=currentRow[cell]*(-1*matrix[otherRows][row])#This will multiply each matrix entry by the opposite of the value we are trying to cancel.
                #currentRow should be a row that we can simply add to the row we are canceling(otherRows) in order to make it row eschlon form
                for canceled in range(row,len(matrix[row])):
                    matrix[otherRows][canceled]=matrix[otherRows][canceled]+currentRow[canceled]
                #Now we have the entirety of this column canceled :)
        return matrix







if __name__=="__main__":
    import random
    print("testing array")
    array=generateMatrix(20)
    for row in array:
        print(row)
        print("\n")
    print("testing addAverages with")
    testArray=[]
    for i in range(20):
        testArray.append(random.randint(15,200))
    print(testArray)
    array = addAverages(array,testArray)
    print(array)
    print("Array in RREF")
    print(convertMatrixAndRREF(array))
