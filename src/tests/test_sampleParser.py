# test_sampleParser.py

import os
from .. import sampleParser

class TestSampleParser:

    def setup(self):
        self.folderName = os.path.join('.', 'tests', 'Export')
        self.parser = sampleParser.SampleParser(self.folderName)

    def test_getDirectoryFiles(self):
        files = self.parser.getDirectoryFiles()
        assert len(files) > 0

    def test_storeFileNamesInDictionary(self):
        files = self.parser.getDirectoryFiles()
        assert len(files) > 0
        for f in files:
            self.parser.storeFileNamesByPatternInDictionary(f)
        sampleDictionary = self.parser.getSampleDictionary()
        assert len(sampleDictionary) == 4

    def test_getListOfContents(self):
        files = self.parser.getDirectoryFiles()
        assert len(files) > 0
        f = files[0]
        assert len( self.parser.getListOfContents(f) ) > 0






