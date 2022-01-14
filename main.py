import pandas as pd

from AcquisitionHelper import *

yearOfStorm = []
oceans = []
dates = []
hours = []
stormsName = []
stormType = []
latCorr = []
longCorr = []
windPower = []
airPressure = []
deaths = []
damagedUsd = []

scrapGeneralInformationOfOcean(oceansURL)

for i in range(2021, 1851, -1):
    scrapDataFromCurrYear(i, 'Atlantic Ocean', yearOfStorm, oceans, dates, hours, windPower, airPressure,
                          stormType, stormsName, latCorr, longCorr)

