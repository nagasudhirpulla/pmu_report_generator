# https://stackoverflow.com/questions/55223489/filter-pandas-dataframe-with-specific-time-of-day-or-hour
from src.config.appConfig import getConfig, getFetchPnts
from src.services.pmuDataFetcher import PmuDataFetcher
from src.services.dummyDataFetcher import DummyDataFetcher
from src.utils.variableTime import VariableTime
import datetime as dt

appConfig = getConfig()
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

# fetcher = PmuDataFetcher(appConfig['host'], appConfig['port'], appConfig['path'],
#                          appConfig['username'], appConfig['password'], appConfig['refMeasId'])

fetcher = DummyDataFetcher()
resDf = fetcher.fetchPntsData(pnts, startTime, endTime, resampleFreq)
resDf.to_excel('data/dump.xlsx')
print('execution done...')