# test_sampleParser.py

import os
from .. import sampleParser

class TestSampleParser:

    def setup(self):
        self.folderName = os.path.join('.', 'tests', 'Export')
        self.parser = sampleParser.SampleParser(self.folderName)

    def test_getDirectoryFiles(self):
        files = self._obtainDirectory()
        assert len(files) > 0

    def test_storeFileNamesByPatternInDictionary(self):
        files = self._obtainDirectory()
        assert len(files) > 0
        for _file in files:
            self.parser.storeFileNamesByPatternInDictionary(_file)
        sampleDictionary = self.parser.getSampleDictionary()
        assert len(sampleDictionary) == 4
        print ("SampleParser: ", sampleDictionary)
        # each item in the dictionary should have two samples for each sample type
        for sample in sampleDictionary.items():
            assert len(sample) == 2

    def test_readFileIntoArray(self):
        files = self._obtainDirectory()
        assert len(files) > 0
        assert len(self.parser.readFileIntoArray(files[0])) > 0

    def _obtainDirectory(self):
        return self.parser.getDirectoryFiles()





