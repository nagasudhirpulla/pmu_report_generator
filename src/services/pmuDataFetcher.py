# -*- coding: utf-8 -*-
"""
Using Popen to communicate with exe file
https://docs.python.org/3.4/library/subprocess.html#subprocess.Popen.communicate
use shlex to parse command string if required
shlex.split(/bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'")
will give
['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]
"""
from subprocess import Popen, PIPE
import datetime as dt
from typing import List, Union
from src.utils.timeUtils import convertEpochMsToDt
import pandas as pd


class PmuDataFetcher():
    def __init__(self, host: str, port: int, path: str, username: str, password: str, refMeasId: int, dataRate: int = 25):
        self.host = host
        self.port = port
        self.path = path
        self.username = username
        self.password = password
        self.refMeasId = refMeasId
        self.dataRate = dataRate

    def __fetchRawPntData(self, pntId: int, startTime: dt.datetime, endTime: dt.datetime) -> pd.Series:
        command = "./PMUDataAdapter.exe"
        args = [command]
        args.extend(["--meas_id", str(pntId)])
        args.extend(
            ["--from_time", dt.datetime.strftime(startTime, '%Y_%m_%d_%H_%M_%S')])
        args.extend(
            ["--to_time", dt.datetime.strftime(endTime, '%Y_%m_%d_%H_%M_%S')])
        args.extend(["--host", self.host])
        args.extend(["--port", str(self.port)])
        args.extend(["--path", self.path])
        args.extend(["--username", self.username])
        args.extend(["--password", self.password])
        args.extend(["--ref_meas_id", str(self.refMeasId)])
        args.extend(["--data_rate", str(self.dataRate)])
        proc = Popen(args, stdout=PIPE)
        try:
            outs, errs = proc.communicate()
        except:
            proc.kill()
            return []
        resp = outs.decode("utf-8")
        # split the response by comma
        respSegs: List[str] = resp.split(',')
        timestamps: List[dt.datetime] = []
        vals: List[float] = []
        try:
            for samplInd in range(0, int(len(respSegs)/2)):
                ts = convertEpochMsToDt(float(respSegs[2*samplInd]))
                val = float(respSegs[2*samplInd+1])
                timestamps.append(ts)
                vals.append(val)
            data = pd.Series(vals, index=timestamps)
            return data
        except Exception as inst:
            print(inst)
            return pd.Series()

    def __resampleData(self, data: pd.Series, resampleFreq: str, aggStrategy: str) -> pd.Series:
        if pd.isna(resampleFreq):
            return data
        if not (resampleFreq.lower() in ['s', 'm', 'b', 'h', 'd']):
            return data
        if pd.isna(aggStrategy) or (aggStrategy.lower() == 'raw'):
            return data

        # storing series labels
        seriesName = data.name
        indName = data.index.name

        # changing series labels
        data.name = 'vals'
        data.index.name = 'times'
        data = data.reset_index()
        # modify times as per resampleFreq
        # https://stackoverflow.com/questions/43400331/remove-seconds-and-minutes-from-a-pandas-dataframe-column
        if resampleFreq.lower() == 'd':
            data = data.assign(times=data.times.dt.round('D'))
        elif resampleFreq.lower() == 'h':
            data = data.assign(times=data.times.dt.round('H'))
        elif resampleFreq.lower() == 'm':
            data = data.assign(times=data.times.dt.round('min'))
        elif resampleFreq.lower() == 's':
            data = data.assign(times=data.times.dt.round('S'))
        elif resampleFreq.lower() == 'b':
            data = data.assign(times=data.times.dt.round('min'))
            data.times = data.times.map(
                lambda x: x.replace(minute=(x.minute - x.minute % 15)))

        # aggregate the samples based on times
        if aggStrategy.lower() == 'snap':
            data = data.groupby('times', as_index=False).first()
        elif aggStrategy.lower() == 'average':
            data = data.groupby('times', as_index=False).mean()
        data = pd.Series(data.vals, index=data.times)

        # restore original labels
        data.name = seriesName
        data.index.name = indName
        return data

    def __getFetchWindows(self, startTime: dt.datetime, endTime: dt.datetime, fetchWindow: dt.timedelta) -> List[List[dt.datetime]]:
        resWindows: List[List[dt.datetime]] = []
        # check if start time is greater than end time
        if startTime > endTime:
            return resWindows
        # if window width is 0, send start and end times without splitting
        if fetchWindow.total_seconds == 0:
            return [[startTime, endTime]]
        
        winStartTime = startTime
        winEndTime = winStartTime + fetchWindow
        while winEndTime <= endTime:
            if winEndTime == endTime:
                resWindows.append([winStartTime, winEndTime])
            else:
                sampleDelta = dt.timedelta(microseconds=40000)
                resWindows.append([winStartTime, winEndTime-sampleDelta])
            winStartTime = winEndTime
            winEndTime = winEndTime + fetchWindow
        return resWindows

    def fetchPntData(self, pntId: int, startTime: dt.datetime, endTime: dt.datetime, fetchWindow: dt.timedelta, resampleFreq: str, aggStrategy: str) -> pd.Series:
        # initialize empty pandas series
        resData = pd.Series()
        # get fetch windows
        fetchWins: List[List[dt.datetime]] = self.__getFetchWindows(
            startTime, endTime, fetchWindow)
        # iterate through fetch windows for fetching data
        for fetchWin in fetchWins:
            # fetch raw data
            data = self.__fetchRawPntData(pntId, fetchWin[0], fetchWin[1])
            # resample raw data
            data = self.__resampleData(data, resampleFreq, aggStrategy)
            # append data to the result series
            resData = resData.append(data)
        return resData
