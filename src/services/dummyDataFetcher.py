import datetime as dt
from typing import List
import pandas as pd
import random
from src.typeDefs.fetchPnt import FetchPnt
from src.utils.timeUtils import getSampleDelta, getSampleTimestamps


class DummyDataFetcher():
    def fetchPntData(self, pntId: int, startTime: dt.datetime, endTime: dt.datetime, resampleFreq: str) -> pd.Series:
        currTime = startTime
        # initialize result dataframe with ideal index
        idealTimestamps: List[dt.datetime] = getSampleTimestamps(
            startTime, endTime, resampleFreq)
        vals: List[float] = [random.random() for x in idealTimestamps]
        return pd.Series(vals, index=idealTimestamps)

    def fetchPntsData(self, pnts: List[FetchPnt], startTime: dt.datetime, endTime: dt.datetime, resampleFreq: str) -> pd.DataFrame:
        # initialize result dataframe with ideal index
        idealTimestamps = getSampleTimestamps(startTime, endTime, resampleFreq)
        resDf = pd.DataFrame(index=idealTimestamps)
        # iterate through all the points and populate the result dataframe
        for pnt in pnts:
            pntId: int = pnt['id']
            pntName: int = pnt['name']
            pntData = self.fetchPntData(
                pntId, startTime, endTime, resampleFreq)
            resDf['{0}|{1}'.format(pntId, pntName)] = pntData
        return resDf
