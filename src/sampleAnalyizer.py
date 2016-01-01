# sampleAnalyzer.py

import pandas as pd
import numpy as np
import pprint

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
class SampleAnalyizer():
    def __init__(self):
        self.tests = Vividict()

    def printVariables(self):
        print ("cut", self.cut)
        print ("plot_data:", self.plot_data)
        print ("plot_data2:", self.plot_data)
        print ("arr_signal:", self.arr_signal)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.tests)

    def setVariables(self, value=""):
        self.pname = value
        self.cut = value
        self.arr_signal = []
        self.extract_frequency = "2440000000"
        self.signalCount = 0
        self.count = 0
        self.threshold = -5.0
        self.totalSignal = 120
        self.plot_data = []
        self.plot_data2 = []
        self.waterFall = []
        self.sortedSignals = []
        self.results = 0

    def extractLines(self, df):
        """ Let Pandas do the heavy lifting here """
        # checks if line[0] == self.extract_frequency
        accepted_df = df[df.ix[:,0] == int(self.extract_frequency)]
        # accepted_df.sort_values(inplace=True)

        # count up the rows in the entire datatable
        self.count = len(accepted_df)
        # print (accepted_df)
        # checks if line[2] >= self.threshold and finds length

        # determine the count of values in column 2 in the datatable that are equal
        # to or exceed the threshold value
        self.signalCount = len(accepted_df[accepted_df.ix[:,2] >= self.threshold])

        # Modify the data in each row in column 2 in the datatable
        self.arr_signal = (accepted_df.ix[:,2] + 15.0) * 5.0

        # round to two decimal places
        self.arr_signal = np.round(self.arr_signal, decimals=2)
        # print(self.arr_signal)

        print ("self.count: ", self.count)
        print ("self.signalCount: ", self.signalCount)
        self.results = 100.0 * int(10000 * self.signalCount / self.totalSignal) / 10000
        print ("-> ", self.results, "% of signals above ", self.threshold, " dbi ")

    def percent_above_threshold(self, dataframe="", value=""):
        if self.cut != 'theta=90':
            self.plot_data.extend(self.plot_data2)
            self.sortedSignals = sorted(self.arr_signal)
            #print("self.count:", self.count)
            #print("self.signalCount:", self.signalCount)
            #print("self.totalSignal:", self.totalSignal)
            #print("self.signalCount/self.totalSignal:", float(self.signalCount)/self.totalSignal)

            self.results = 100.0 * int(10000 * self.signalCount / self.totalSignal) / 10000
            print ("-> ", self.results, "% of signals above ", self.threshold, " dbi ")
            #print ("self.plot_data:", sorted(self.plot_data), "len:", len(self.plot_data))
            #print ("self.plot_data2:", sorted(self.plot_data2), "len:", len(self.plot_data2))

            self.tests[self.pname][self.cut]["percentAbove"] = self.results/100
            self.tests[self.pname][self.cut]["plot_data"] = self.plot_data

            for index in range(-30,11):
                count = self.countSignals(index)
                self.waterFall.append("%.2f" % (count/121.0 * 83.333))

            self.tests[self.pname][self.cut]["waterFall"] = self.waterFall

            if self.results <= 30:
                print ("- FAIL -")
            else:
                print (" \n")
            self.signalCount = 0

        else:
            print ("Error! No value for pname and/or cut")

    def countSignals(self, index):
        count = 0
        while ( float(self.sortedSignals[count]) >= index):
            count += 1
            if count >= len(self.sortedSignals):
                break
        return count

    def generateDataFrameFromFile(self, filename):
        return pd.read_csv(filename, skiprows=2, delimiter='\t', header=0)
