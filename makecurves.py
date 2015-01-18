#!/usr/bin/env python

import mathlib
import databaselib

if __name__ == "__main__":
    print("Generating matrix")
    array = mathlib.generateMatrix(20)
    print("Querying database")
    low_bracket, mid_bracket, high_bracket = databaselib.getDataTuples("diseasedata.db", "publicationdata")

    # Calculate averages
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

    print "array averages"
    print "low"
    print low_disease_averages
    print "mid"
    print mid_disease_averages
    print "high"
    print high_disease_averages

    # Generate final matricies
    final_low_array = mathlib.addAverages(array, low_disease_averages)
    final_mid_array = mathlib.addAverages(array, mid_disease_averages)
    final_high_array = mathlib.addAverages(array, high_disease_averages)

    print "final matricies"
    print "low"
    print final_low_array
    print "mid"
    print final_mid_array
    print "high"
    print final_high_array

    # TODO generate standard deviations

    print("Lower bracket curve in RREF:\n" + str(mathlib.convertMatrixAndRREF(final_low_array)) + "\n")
    print("Middle bracket curve in RREF:\n" + str(mathlib.convertMatrixAndRREF(final_mid_array)) + "\n")
    print("High bracket curve in RREF:\n" + str(mathlib.convertMatrixAndRREF(final_high_array)) + "\n")
