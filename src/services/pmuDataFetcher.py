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


class PmuDataFetcher():
    def __init__(self, host: str, port: int, path: str, username: str, password: str, refMeasId: int):
        self.host = host
        self.port = port
        self.path = path
        self.username = username
        self.password = password
        self.refMeasId = refMeasId

    def fetchPmuData(self, pntId: int, startTime: dt.datetime, endTime: dt.datetime, dataRate: int = 25) -> List[List[Union[dt.datetime, float]]]:
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
        args.extend(["--data_rate", str(dataRate)])
        proc = Popen(args, stdout=PIPE)
        try:
            outs, errs = proc.communicate()
        except:
            proc.kill()
            return []
        resp = outs.decode("utf-8")
        # split the response by comma
        respSegs: List[str] = resp.split(',')
        data: List[List[Union[dt.datetime, float]]] = []
        try:
            for samplInd in range(0, int(len(respSegs)/2)):
                ts = convertEpochMsToDt(float(respSegs[2*samplInd]))
                val = float(respSegs[2*samplInd+1])
                data.append([ts, val])
            return data
        except Exception as inst:
            print(inst)
            return []
