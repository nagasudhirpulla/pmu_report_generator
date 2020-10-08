import datetime as dt
from typing import List
import pandas as pd
import random


class DummyDataFetcher():
    def fetchData(self, pntId: int, startTime: dt.datetime, endTime: dt.datetime, resampleFreq: str) -> pd.Series:
        currTime = startTime
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
        inds: List[dt.datetime] = []
        vals: List[float] = []
        while currTime <= endTime:
            inds.append(currTime)
            vals.append(random.random())
            currTime = currTime + sampleDelta
        return pd.Series(vals, index=inds)
