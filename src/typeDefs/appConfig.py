from typing import TypedDict
import datetime as dt

class IAppConfig(TypedDict):
    host: str
    port: int
    path: str
    username: str
    password: str
    refMeasId: int
    dumpFolder: str
    dummyFetch: str
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
    sampleAggregationStrategy: str
    resampleFrequency: str
    filenamePrefix: str
