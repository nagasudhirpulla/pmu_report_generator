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


class DummyDataFetcher():
    def fetchPmuData(self, pntId: int, startTime: dt.datetime, endTime: dt.datetime) -> List[List[Union[dt.datetime, float]]]:
        currTime = startTime
        resData: List[List[Union[dt.datetime, float]]] = []
        while currTime <= endTime:
            resData.append([currTime, 0.5])
            currTime = currTime + dt.timedelta(microseconds=40000)
        return resData
