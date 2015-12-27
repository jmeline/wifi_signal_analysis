# test_sampleAnalyzer.py

import os
from ..sampleAnalyizer import SampleAnalyizer

class TestSampleAnalyzer:
    def setup(self):
        self.folderName = os.path.join('.', 'tests', 'Export')
        self.analyzer = SampleAnalyizer()
        self.sampleFile = os.path.join(self.folderName, "NaplesPremium_Spectra1-theta=90.txt")
        self.sampleFile2 = os.path.join(self.folderName, "NaplesPremium_Spectra2-theta=90.txt")

    def _setupSampleDataFrame(self, sampleFile):
        dataframe = self.analyzer.generateDataFrameFromFile(sampleFile)
        return dataframe

    def test_generateDataFrameFromFile(self):
        dataframe = self._setupSampleDataFrame(self.sampleFile)
        assert not dataframe.empty

    def test_generateDataFrameFromFile2(self):
        dataframe = self._setupSampleDataFrame(self.sampleFile2)
        assert not dataframe.empty

    def test_extractLines(self):
        dataframe = self._setupSampleDataFrame(self.sampleFile)
        self.analyzer.setVariables('theta=90')
        self.analyzer.extractLines(dataframe)
        assert self.analyzer.count == 120
        assert self.analyzer.signalCount == 98
        assert self.analyzer.results == 81.66

    def test_extractLines2(self):
        dataframe = self._setupSampleDataFrame(self.sampleFile2)
        self.analyzer.setVariables('theta=90')
        self.analyzer.extractLines(dataframe)
        assert self.analyzer.count == 120
        assert self.analyzer.signalCount == 99
        assert self.analyzer.results == 82.5








