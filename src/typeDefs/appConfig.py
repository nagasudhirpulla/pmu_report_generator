from typing import TypedDict
import datetime as dt


class IAppConfig(TypedDict):
    dummyFetchFlag: str
    host: str
    port: int
    path: str
    username: str
    password: str
    refMeasId: int
    dumpFolder: str
    filenamePrefix: str
    absoluteStartTime: dt.datetime
    varStartYears: float
    varStartMonths: float
    varStartDays: float
    varStartHours: float
    varStartMinutes: float
    varStartSeconds: float
    absoluteEndTime: dt.datetime
    varEndYears: float
    varEndMonths: float
    varEndDays: float
    varEndHours: float
    varEndMinutes: float
    varEndSeconds: float
    fetchWindowDays: float
    fetchWindowHours: float
    fetchWindowMinutes: float
    fetchWindowSeconds: float
    resampleFrequency: str
    sampleAggregationStrategy: str
