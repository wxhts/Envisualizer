from __future__ import division
from itertools import product
import pandas as pd
from createControls import createControls


class EnVisualize(object):
    # Methods to calculate 1536-well plate statistics such as HPE and ZPE percent CVs, signal to background ratio,
    # and Z-prime from Envision plate reader data. Input "plate" should be a pandas DataFrame with row(1 - 32) and
    # column(1-48) indexes.

    def __init__(self, plate, compounds_path, controls_path, control_inh=False):

        self.control_inh = control_inh
        self.plate = plate
        self.avg_hpe = 0
        self.avg_zpe = 0
        self.std_hpe = 0
        self.std_zpe = 0
        self.compounds = pd.read_csv(compounds_path)    # Indexed compound file

        if self.control_inh:
            self.controls = createControls(controls_path,standards=True)
        else:
            self.controls = createControls(controls_path)

    def __control_results(self, controls):
        """Input: controls is a list of tuples of coordinates
           Output: a Series of results from the input control region"""
        area = []
        for i in controls:
            well = self.plate[(self.plate['Row'] == i[1]) & (self.plate['Column'] == i[0])]
            area.append(well)

        smushed_area = pd.concat(area)
        series_results = pd.Series(smushed_area['Result'])
        return series_results

    def CV(self, region):
        """Calculates percent CV of HPE and ZPE plate regions"""

        region = region.lower()
        if region == 'hpe':

            hpe_controls = self.controls[0]
            hpe_results = self.__control_results(hpe_controls)

            self.avg_hpe = hpe_results.mean()
            self.std_hpe = hpe_results.std()

            percentHPECV = round(100*(self.std_hpe/self.avg_hpe), 2)
            return percentHPECV

        elif region == 'zpe':

            zpe_controls = self.controls[1]
            zpe_results = self.__control_results(zpe_controls)

            self.avg_zpe = zpe_results.mean()
            self.std_zpe = zpe_results.std()

            percentZPECV = round(100*(self.std_zpe/self.avg_zpe), 2)
            return percentZPECV

    def signalToBackground(self):
        """Calculates the signal to background ratio of the plate"""

        sob = round((self.avg_zpe/self.avg_hpe), 2)
        return sob

    def zPrime(self):
        """Calculates the Z-prime of the plate"""

        numerator = 3 * (self.std_zpe + self.std_hpe)
        denominator = abs(self.avg_zpe - self.avg_hpe)
        prime = 1 - (numerator/denominator)

        zprime = round(prime, 2)
        return zprime

    def inhibitorControl(self):
        """Calculates the average percent inhibition of the inhibitor control regions"""
        if self.control_inh:

            std_controls = self.controls[2]
            std_results = self.__control_results(std_controls)

            perc_INH = []
            for i in std_results:
                percent_INH = round(100 - (100 * ((i - self.avg_hpe)/(self.avg_zpe - self.avg_hpe))), 2)
                perc_INH.append(percent_INH)

            controlMean = np.mean(perc_INH)
            return controlMean
        else:
            pass

    def percentInhibition(self):
        """Calculates the percent inhibition for each well in the sample region of the plate and returns with values
        already added to self.plate DataFrame
        IMPLEMENT IN SUBCLASSES"""

        pass

    def compoundAdder(self, compound_barcode):
        """Join the Client_ID to each assay plate using a reference file of compound positions"""

        compound_plate = self.compounds[(self.compounds['Barcode'] == compound_barcode)]
        self.plate = pd.merge(self.plate, compound_plate, left_on=['Row', 'Column'], right_on=['Row', 'Column'])

        return self.plate


class EnVisualize1536(EnVisualize):

    def __init__(self):
        EnVisualize.__init__(self, plate, compounds_path, controls_path, control_inh=False)

    def percentInhibition(self):
        """Calculates the percent inhibition for each well in the sample region of the plate and returns with values
        already added to self.plate Dataframe"""

        pd.set_option('mode.chained_assignment', None)  # Silences pandas SettingWithCopy warning

        samplesX = range(1, 33)
        samplesY = range(5, 45)

        rawData = []
        for x, y in product(samplesX, samplesY):
            result = self.plate[(self.plate['Row'] == x) & (self.plate['Column'] == y)]
            rawData.append(result)

        samples = pd.concat(rawData)
        samplesSeries = pd.Series(samples['Result'], index=samples.index)

        inhibs = []
        for i in samplesSeries:
            percentInhib = round(100 - (100 * ((i - self.avg_hpe)/(self.avg_zpe - self.avg_hpe))), 2)
            inhibs.append((percentInhib))

        self.plate['Percent Inhibition'] = pd.Series(inhibs, index=samplesSeries.index)
        return self.plate


class EnVisualize384(EnVisualize):

    def __init__(self):
        EnVisualize.__init__(self, plate, compounds_path, controls_path, control_inh=False)

    def percentInhibition(self):
        """Calculates the percent inhibition for each well in the sample region of the plate and returns with values
        already added to self.plate Dataframe"""

        pd.set_option('mode.chained_assignment', None)  # Silences pandas SettingWithCopy warning

        samplesX = range(1, 17)
        samplesY = range(3, 23)

        rawData = []
        for x, y in product(samplesX, samplesY):
            result = self.plate[(self.plate['Row'] == x) & (self.plate['Column'] == y)]
            rawData.append(result)

        samples = pd.concat(rawData)
        samplesSeries = pd.Series(samples['Result'], index=samples.index)

        inhibs = []
        for i in samplesSeries:
            percentInhib = round(100 - (100 * ((i - self.avg_hpe)/(self.avg_zpe - self.avg_hpe))), 2)
            inhibs.append((percentInhib))

        self.plate['Percent Inhibition'] = pd.Series(inhibs, index=samplesSeries.index)
        return self.plate
