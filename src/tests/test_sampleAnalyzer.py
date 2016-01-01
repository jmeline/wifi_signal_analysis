# test_sampleAnalyzer.py

import os
from ..sampleAnalyizer import SampleAnalyizer

class TestSampleAnalyzer:
    def setup(self):
        self.folderName = os.path.join('.', 'tests', 'Export')
        self.analyzer = SampleAnalyizer()
        self.sampleFile = os.path.join(self.folderName, "NaplesPremium_Spectra1-theta=90.txt")
        self.sampleFile2 = os.path.join(self.folderName, "NaplesPremium_Spectra2-theta=90.txt")

        self.sampleFileExpectedOutput = [55.68,44.54,29.23,10.58,2.88,13.02,21.58,24.24,25.06,32.10,44.96,56.37,63.30,65.35,62.79,57.17,53.29,56.23,62.31,66.19,66.72,65.62,65.74,67.55,68.25,65.33,58.40,51.14,50.93,56.64,62.14,66.29,69.99,73.11,74.56,73.64,70.63,66.48,62.04,57.72,54.44,53.78,55.12,55.58,53.20,48.75,46.18,48.59,53.36,57.55,61.27,65.84,71.55,77.37,82.08,84.89,85.39,83.38,78.98,72.89,66.97,63.61,62.80,61.86,58.59,53.13,49.05,50.63,55.46,58.78,58.82,55.82,50.89,45.49,41.21,40.14,43.70,49.37,52.93,51.56,44.22,35.90,42.99,57.49,66.51,68.56,64.52,58.19,58.87,67.55,75.51,79.58,80.09,78.33,75.84,74.16,74.07,75.10,75.99,75.68,73.99,71.86,70.90,72.02,74.65,77.75,80.65,82.98,84.52,85.27,85.47,85.44,85.22,84.56,83.19,81.01,78.06,74.37,69.77,63.77]
        self.sampleFile2ExpectedOutput = [50.45,50.71,53.24,56.72,60.28,63.44,65.95,67.73,68.98,70.17,71.83,74.20,77.17,80.56,84.08,87.25,89.42,90.32,90.18,89.63,89.10,88.47,87.29,85.52,83.47,81.33,78.82,75.87,73.56,73.41,75.13,77.06,78.57,80.43,83.15,86.05,87.95,88.36,87.31,85.12,81.91,77.84,73.08,67.83,61.82,54.95,49.87,52.01,59.79,67.12,71.80,74.38,76.31,78.63,81.14,82.91,83.08,81.49,78.42,74.86,71.99,70.48,70.07,70.09,69.83,68.49,65.20,59.80,54.51,54.22,58.99,63.18,63.09,57.39,46.17,34.53,34.34,40.32,42.11,38.24,31.12,26.09,26.31,29.44,33.93,38.68,41.25,39.39,32.77,26.75,31.54,41.56,48.25,50.55,50.18,49.77,50.79,52.48,53.94,55.80,59.26,64.05,68.55,71.54,72.74,72.53,71.62,70.70,70.28,70.65,71.71,73.08,74.18,74.55,73.87,71.94,68.62,63.93,58.38,53.28]

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
        # Check to make sure that every value is the same as the output of the perl script
        assert (self.analyzer.arr_signal.isin( self.sampleFileExpectedOutput )).all()

    def test_extractLines2(self):
        dataframe = self._setupSampleDataFrame(self.sampleFile2)
        self.analyzer.setVariables('theta=90')
        self.analyzer.extractLines(dataframe)
        assert self.analyzer.count == 120
        assert self.analyzer.signalCount == 99
        assert self.analyzer.results == 82.5
        assert (self.analyzer.arr_signal.isin( self.sampleFile2ExpectedOutput )).all()









