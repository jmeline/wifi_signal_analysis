
class SampleParser():
    """ Gathers files that match user specific expression types """

    def __init__(self, folderName):
        self.folderName = folderName
        self.fileHash = defaultdict(list)

    def getDirectoryFiles(self):
        if self.folderName:
            onlyfiles = [ f for f in listdir(self.folderName) \
                    if isfile(join(self.folderName,f)) ]
        else:
            print ("Path Not Found")
        return onlyfiles

    def printDirectory(self):
        """ Debugging/helper function """
        if self.folderName:
            for i in listdir(self.folderName):
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
        path = folderName + fileName
        print (path)
        with open(path, 'r') as fin:
            for line in fin:
                arrayList.append(' '.join(line.split()).split())
        return arrayList

    def generateDataFrameFromFile(self, filename):
        path = folderName + filename
        return pd.read_csv(path, skiprows=2, delimiter='\t', header=0)


