# main.py
from sampleParser import SampleParser as SampleExtractor
from sampleAnalyizer import SampleAnalyizer

## Modify your path ##
path = './Export/'
## ## ## ## ## ## ## #

def main():
    ## Collect all of the samples and organize them together into a dictionary.
    extractor = SampleExtractor(path)
    currentFilesInDirectory = extractor.getDirectoryFiles()
    for _file in currentFilesInDirectory:
        extractor.storeFileNamesByPatternInDictionary(_file)
    sampleDictionary = extractor.getSampleDictionary()
    # Debugging
    # f.printDirectory()

    ## Begin analyzing data
    analyzer = SampleAnalyizer()
    for key, value in sorted(sampleDictionary.items()):
        print ("ValueArr: ", value)
        for filename in value:
           if not key is 'efficien':
               # arrList = f.getListOfContents(filename)
               dataframe = extractor.generateDataFrameFromFile(filename)
               print ("Key: ", key)
               # print ("arrList: ", arrList, " key: ", key)
               analyzer.percent_above_threshold(dataframe, key)

    #mf.printVariables()

    ## Begin graphing data

if __name__ == '__main__':
    main()
