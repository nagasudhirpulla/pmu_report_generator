import datetime as dt
import pandas as pd
from typing import List


def convertEpochMsToDt(epochMs: float) -> dt.datetime:
    timeObj = dt.datetime.fromtimestamp(epochMs/1000)
    return timeObj


def getSampleDelta(resampleFreq: str) -> dt.timedelta:
    sampleDelta = dt.timedelta(microseconds=40000)
    if not pd.isna(resampleFreq):
        if resampleFreq.lower() == 's':
            sampleDelta = dt.timedelta(seconds=1)
        elif resampleFreq.lower() == 'm':
            sampleDelta = dt.timedelta(minutes=1)
        elif resampleFreq.lower() == 'b':
            sampleDelta = dt.timedelta(minutes=15)
        elif resampleFreq.lower() == 'h':
            sampleDelta = dt.timedelta(hours=1)
        elif resampleFreq.lower() == 'd':
            sampleDelta = dt.timedelta(days=1)
    return sampleDelta


def getSampleTimestamps(startTime: dt.datetime, endTime: dt.datetime, resampleFreq: str) -> List[dt.datetime]:
    sampleDelta = getSampleDelta(resampleFreq)
    times: List[dt.datetime] = []
    if startTime > endTime:
        return times
    currTime = startTime
    while currTime <= endTime:
        times.append(currTime)
        currTime = currTime+sampleDelta
    return times
