import os
import re

class SampleParser():
    """ Gathers files that match user specific expression types and groups them into a dictionary"""

    def __init__(self, folderName):
        self.folderName = folderName
        self._sampleDictionary = {}

    def getDirectoryFiles(self):
        """ Directory given to the constructor is scanned for files. An array of found files is returned """
        filesInDirectory = []
        if not self.folderName:
            return filesInDirectory
        filesInDirectory = [ f for f in os.listdir(self.folderName) \
            if os.path.isfile(os.path.join(self.folderName,f)) ]
        return filesInDirectory

    def printDirectory(self):
        print ("start DEbugging")
        """ Debugging/helper function """
        _directoryFiles = self.getDirectoryFiles()
        print ("DirectoryFiles: ", len(_directoryFiles))
        for _file in _directoryFiles:
            print (_file)

        print ("sampleDictionary: ", len(self._sampleDictionary))
        for k,v in self._sampleDictionary.items():
            print ("%s: %s" % (k,v))
        print ("End DEbugging")

    def storeFileNamesByPatternInDictionary(self, fileName):
        # Regular Expression Patterns
        eff_pat = r'efficien'
        phi0_pat = r'phi=0'
        phi90_pat = r'phi=90'
        theta90_pat = r'theta=90'

        samplePatterns = [theta90_pat, phi0_pat, phi90_pat, eff_pat]
        for pattern in samplePatterns:
            match = re.search(pattern, fileName)
            if match and pattern in self._sampleDictionary.keys():
                self._sampleDictionary[pattern].append(fileName)
            elif match:
                self._sampleDictionary[pattern] = [fileName]

    def getSampleDictionary(self):
        return self._sampleDictionary

    def readFileIntoArray(self, fileName):
        contents = []
        path = os.path.join(self.folderName, fileName)
        print (path)
        with open(path, 'r') as fin:
            for line in fin:
                contents.append(' '.join(line.split()).split())
        return contents

