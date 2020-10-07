import datetime as dt
def convertEpochMsToDt(epochMs: float) -> dt.datetime:
    timeObj = dt.datetime.fromtimestamp(epochMs/1000)
    return timeObj