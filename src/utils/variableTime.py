import datetime as dt
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta


class VariableTime():
    yearsOffset: float = np.nan
    monthsOffset: float = np.nan
    daysOffset: float = np.nan
    hoursOffset: float = np.nan
    minutesOffset: float = np.nan
    secondsOffset: float = np.nan
    absoluteTime: dt.datetime = dt.datetime.now()

    def __init__(self, yearsOffset: float, monthsOffset: float, daysOffset: float, hoursOffset: float, minutesOffset: float, secondsOffset: float, absoluteTime: dt.datetime):
        self.yearsOffset = yearsOffset
        self.monthsOffset = monthsOffset
        self.daysOffset = daysOffset
        self.hoursOffset = hoursOffset
        self.minutesOffset = minutesOffset
        self.secondsOffset = secondsOffset
        self.absoluteTime = absoluteTime

    def getTimeObj(self) -> dt.datetime:
        absTime = self.absoluteTime
        nowTime = dt.datetime.now()

        # Make millisecond component as zero for the absolute time and now time
        absTime = absTime.replace(microsecond=0)
        nowTime = nowTime.replace(microsecond=0)
        resultTime = nowTime

        # Add offsets to current time as per the settings
        if not pd.isna(self.yearsOffset):
            resultTime = resultTime + \
                relativedelta(years=int(self.yearsOffset))
        if not pd.isna(self.monthsOffset):
            resultTime = resultTime + \
                relativedelta(months=int(self.monthsOffset))
        if not pd.isna(self.daysOffset):
            resultTime = resultTime + dt.timedelta(days=self.daysOffset)
        if not pd.isna(self.hoursOffset):
            resultTime = resultTime + dt.timedelta(hours=self.hoursOffset)
        if not pd.isna(self.minutesOffset):
            resultTime = resultTime + dt.timedelta(minutes=self.minutesOffset)
        if not pd.isna(self.secondsOffset):
            resultTime = resultTime + dt.timedelta(seconds=self.secondsOffset)

        # Set absolute time settings to the result time
        if pd.isna(self.yearsOffset):
            resultTime = resultTime + \
                relativedelta(years=(absTime.year - resultTime.year))
        if pd.isna(self.monthsOffset):
            resultTime = resultTime + \
                relativedelta(months=(absTime.month - resultTime.month))
        if pd.isna(self.daysOffset):
            resultTime = resultTime + \
                dt.timedelta(days=(absTime.day - resultTime.day))
        if pd.isna(self.hoursOffset):
            resultTime = resultTime + \
                dt.timedelta(hours=(absTime.hour - resultTime.hour))
        if pd.isna(self.minutesOffset):
            resultTime = resultTime + \
                dt.timedelta(minutes=(absTime.minute - resultTime.minute))
        if pd.isna(self.secondsOffset):
            resultTime = resultTime + \
                dt.timedelta(seconds=(absTime.second - resultTime.second))
        return resultTime
