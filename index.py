# https://stackoverflow.com/questions/55223489/filter-pandas-dataframe-with-specific-time-of-day-or-hour
from src.config.appConfig import getConfig, getFetchPnts
from src.services.pmuDataFetcher import PmuDataFetcher
from src.services.dummyDataFetcher import DummyDataFetcher
from src.utils.variableTime import VariableTime
import datetime as dt
import pandas as pd
import os
import argparse

# get an instance of argument parser from argparse module
parser = argparse.ArgumentParser()
# setup config file path input argument
configPath = 'config.xlsx'
configSheet = 'config'
parser.add_argument('--configPath', help="Enter path for config file",
                    default=configPath)
parser.add_argument('--configSheet', help="Enter path for config file",
                    default=configSheet)
# get the dictionary of command line inputs entered by the user
args = parser.parse_args()
# access each command line input from the dictionary
configPath = args.configPath
configSheet = args.configSheet

appConfig = getConfig(configFilename=configPath, sheetName=configSheet)
pnts = getFetchPnts()

startVarTime = VariableTime(appConfig["varStartYears"], appConfig["varStartMonths"], appConfig["varStartDays"],
                            appConfig["varStartHours"], appConfig["varStartMinutes"], appConfig["varStartSeconds"], appConfig["absoluteStartTime"])
endVarTime = VariableTime(appConfig["varEndYears"], appConfig["varEndMonths"], appConfig["varEndDays"],
                          appConfig["varEndHours"], appConfig["varEndMinutes"], appConfig["varEndSeconds"], appConfig["absoluteEndTime"])

startTime = startVarTime.getTimeObj()
endTime = endVarTime.getTimeObj()

fetchWindow = dt.timedelta(days=appConfig["fetchWindowDays"], hours=appConfig["fetchWindowHours"],
                           minutes=appConfig["fetchWindowMinutes"], seconds=appConfig["fetchWindowSeconds"])
resampleFreq = appConfig["resampleFrequency"]
aggStrategy = appConfig["sampleAggregationStrategy"]

# fetch dataframe  from service
isDummyFetch = (
    not(pd.isna(appConfig["dummyFetchFlag"])) and appConfig["dummyFetchFlag"] == 1)

if isDummyFetch:
    fetcher = DummyDataFetcher()
    resDf = fetcher.fetchPntsData(pnts, startTime, endTime, resampleFreq)
else:
    fetcher = PmuDataFetcher(appConfig["host"], appConfig["port"], appConfig["path"],
                             appConfig["username"], appConfig["password"], appConfig["refMeasId"])
    resDf = fetcher.fetchPntsData(
        pnts, startTime, endTime, fetchWindow, resampleFreq, aggStrategy)

# generate the dumpfilePath
dumpFolder = appConfig["dumpFolder"]
filenamePrefix = appConfig["filenamePrefix"]
startTimeStr = dt.datetime.strftime(startTime, '%Y_%m_%d')
dumpFilePath = os.path.join(
    dumpFolder, '{0}{1}.xlsx'.format(filenamePrefix, startTimeStr))

# write to file at the desired file path
resDf.to_excel(dumpFilePath)

print("report generation done!")
