from src.config.appConfig import getConfig
from src.services.pmuDataFetcher import PmuDataFetcher

appConfig = getConfig()

fetcher = PmuDataFetcher(appConfig['host'], appConfig['port'], appConfig['path'],
                         appConfig['username'], appConfig['password'], appConfig['refMeasId'])
dataRate = 25

# https://stackoverflow.com/questions/55223489/filter-pandas-dataframe-with-specific-time-of-day-or-hour
