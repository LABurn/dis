#!/usr/bin/env python

import mathlib
import databaselib

if __name__ == "__main__":
    print("Generating matrix")
    array = mathlib.generateMatrix(20)
    print("Querying bullshit")
    low_bracket, mid_bracket, high_bracket = databaselib.getDataTuples("diseasedata.db", "publicationdata")

    low_disease_averages = []
    for i in range(20):
        sum = 0
        for dis in range(len(low_bracket)):
            sum += low_bracket[dis][i][1]
        low_disease_averages.append(float(sum) / float(len(low_bracket)))

    mid_disease_averages = []
    for i in range(20):
        sum = 0
        for dis in range(len(mid_bracket)):
            sum += mid_bracket[dis][i][1]
        mid_disease_averages.append(float(sum) / float(len(mid_bracket)))

    high_disease_averages = []
    for i in range(20):
        sum = 0
        for dis in range(len(high_bracket)):
            sum += high_bracket[dis][i][1]
        high_disease_averages.append(float(sum) / float(len(high_bracket)))

    #array = mathlib.addAverages(array,disease_averages)
    # TODO generate standard deviations
    print("Lower bracket curve in RREF:")
    print(mathlib.convertMatrixAndRREF(low_disease_averages))
    print("Middle bracket curve in RREF:")
    print(mathlib.convertMatrixAndRREF(mid_disease_averages))
    print("High bracket curve in RREF:")
    print(mathlib.convertMatrixAndRREF(high_disease_averages))
