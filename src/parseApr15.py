from __future__ import print_function
from collections import defaultdict
from os import listdir
from os.path import isfile, join

import pandas as pd
import re
import pprint

## Modify your path ##
myPath = './Export/'
## ## ## ## ## ## ## #

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

class FileExtractor():
    def __init__(self, myPath):
        self.myPath = myPath
        self.fileHash = defaultdict(list)
    def getDirectoryFiles(self):
        if self.myPath:
            onlyfiles = [ f for f in listdir(self.myPath) \
                    if isfile(join(self.myPath,f)) ]
        else:
            print ("Path Not Found")
        return onlyfiles
    def printDirectory(self):
        if self.myPath:
            for i in listdir(self.myPath):
                print (i)
            if self.fileHash:
                for k,v in sorted(self.fileHash.items()):
                    print ("%s: %s" % (k,v)) 
    def extractFiles(self, fileName):
        # Regular Expression Patterns
        eff_pat = r'efficien'
        phi0_pat = r'phi=0'
        phi90_pat = r'phi=90'
        theta90_pat = r'theta=90'

        pattern = [theta90_pat, phi0_pat, phi90_pat, eff_pat]
        for p in pattern:
            match = re.search(p, fileName)
            if match:
               self.fileHash[p].append(fileName)
    def returnFileHash(self):
        return self.fileHash
    def getListOfContents(self, fileName):
        arrayList = []
        path = myPath + fileName
        print (path)
        with open(path, 'r') as fin:
            for line in fin:
                arrayList.append(' '.join(line.split()).split())
        return arrayList        

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
    def extractLines(self, lines):
        df = pd.DataFrame(lines)
        print (df)
        for line in lines:
            if len(line) > 1:
                if line[0] == self.extract_frequency:
                    #print ("piece:", line)
                    #print("line[0]:", line[0])
                    #print("line[2]:", line[2],)
                    #cmpV = float(line[2])
                    #print(cmpV, ">=", self.threshold, ":", cmpV >= self.threshold  )

                    self.count += 1
                    if float(line[2]) >= self.threshold:
                        self.signalCount += 1
                    self.arr_signal.append(line[2])
                    if self.cut == 'theta=90':
                        self.plot_data.append("%.2f" % ((float(line[2]) + 15.0) * 5.0))
                    elif self.count <= 60: 
                        self.plot_data.append("%.2f" % (((float(line[2]) + 15.0) * 5.0)))
                    else:
                        self.plot_data2.append("%.2f" % (((float(line[2]) + 15.0) * 5.0)))
    def countSignals(self, index):
        count = 0
        while ( float(self.sortedSignals[count]) >= index):
            count += 1
            if count >= len(self.sortedSignals):
                break
            return count
    def percent_above_threshold(self, lines ="", value=""):
        if value and lines:
            self.setVariables(value)
            self.extractLines(lines)

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

def main():
    f = FileExtractor(myPath)
    for i in f.getDirectoryFiles():
        f.extractFiles(i)
        # f.printDirectory()

    mf = MathFunctions()
    for key, valueArr in sorted(f.returnFileHash().items()): 
       for index in valueArr:
           if not key is 'efficien':
               arrList = f.getListOfContents(index)
               # print ("arrList: ", arrList, " key: ", key)
               mf.percent_above_threshold(arrList, key)

    #mf.printVariables()

if __name__ == '__main__':
    main()
