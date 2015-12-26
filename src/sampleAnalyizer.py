import pandas as pd
import pprint

# To emulate perl's native ability to dynamically create
# data structures: Perl Autovivification allows a programmer
# to refer to a structured variable, and arbitrary sub-elements
# of that structured variable, without expressly declaring the
# existence of variable and its complete structure beforehand.

# More info at: https://en.wikipedia.org/wiki/Autovivification
# Tree = lambda:defaultdict(Tree)
# t = Tree()

# http://stackoverflow.com/questions/635483/
# what-is-the-best-way-to-implement-nested-
# dictionaries-in-python/19829714#19829714
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
class MathFunctions():
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
        copy_df = df

        print (df)
        # checks if line[0] == self.extract_frequency

        accepted_df = df[df.ix[:,0] == int(self.extract_frequency)]
        self.count = len(accepted_df)
        # checks if line[2] >= self.threshold and finds length
        self.signalCount = len(accepted_df[accepted_df.ix[:,2] >= self.threshold])
        self.arr_signal = accepted_df.ix[:,2]
        #for line in lines:
        #    if len(line) > 1:
        #        if line[0] == self.extract_frequency:
        #            #print ("piece:", line)
        #            #print("line[0]:", line[0])
        #            #print("line[2]:", line[2],)
        #            #cmpV = float(line[2])
        #            #print(cmpV, ">=", self.threshold, ":", cmpV >= self.threshold  )

        #            self.count += 1
        #            if float(line[2]) >= self.threshold:
        #                self.signalCount += 1
        #            self.arr_signal.append(line[2])
        #            if self.cut == 'theta=90':
        #                self.plot_data.append("%.2f" % ((float(line[2]) + 15.0) * 5.0))
        #            elif self.count <= 60:
        #                self.plot_data.append("%.2f" % (((float(line[2]) + 15.0) * 5.0)))
        #            else:
        #                self.plot_data2.append("%.2f" % (((float(line[2]) + 15.0) * 5.0)))
    def countSignals(self, index):
        count = 0
        while ( float(self.sortedSignals[count]) >= index):
            count += 1
            if count >= len(self.sortedSignals):
                break
            return count
    def percent_above_threshold(self, dataframe ="", value=""):
        if value and dataframe.any:
            self.setVariables(value)
            self.extractLines(dataframe)

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

