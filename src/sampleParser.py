import os
import re

class SampleParser():
    """ Gathers files that match user specific expression types """

    def __init__(self, folderName):
        self.folderName = folderName
        self._sampleDictionary = {}

    def getDirectoryFiles(self):
        if self.folderName:
            onlyfiles = [ f for f in os.listdir(self.folderName) \
                    if os.path.isfile(os.path.join(self.folderName,f)) ]
        else:
            print ("Path Not Found")
        return onlyfiles

    def printDirectory(self):
        """ Debugging/helper function """
        if self.folderName:
            for i in listdir(self.folderName):
                print (i)
            if self._sampleDictionary:
                for k,v in sorted(self._sampleDictionary.items()):
                    print ("%s: %s" % (k,v))

    def storeFileNamesByPatternInDictionary(self, fileName):
        # Regular Expression Patterns
        eff_pat = r'efficien'
        phi0_pat = r'phi=0'
        phi90_pat = r'phi=90'
        theta90_pat = r'theta=90'

        pattern = [theta90_pat, phi0_pat, phi90_pat, eff_pat]
        for p in pattern:
            match = re.search(p, fileName)
            if match:
               self._sampleDictionary[p] = fileName

    def getSampleDictionary(self):
        return self._sampleDictionary

    def getListOfContents(self, fileName):
        arrayList = []
        path = os.path.join(self.folderName, fileName)
        print (path)
        with open(path, 'r') as fin:
            for line in fin:
                arrayList.append(' '.join(line.split()).split())
        return arrayList

    def generateDataFrameFromFile(self, filename):
        path = folderName + filename
        return pd.read_csv(path, skiprows=2, delimiter='\t', header=0)


