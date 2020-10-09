## Description
This is a python script that fetches data of user defined points from the PMU historian API and dumps the data as an excel file at a user defined folder location

## Installation
* Ensure python (above version 3) is installed in the computer
* You may have to setup system environment variable 'PATH' or 'Path', such that you can access 'python' command from command line
* Keep the 'PMUDataAdapter.exe' file in the same folder location of index.py file
* Ensure the 'config.xlsx' file in the same folder location of index.py file. You can use 'config_dummy.xlsx' to create 'config.xlsx' file
* run 'setup_env.bat' file. This should create a folder named 'project_env'

## Running this script
* Mention all the configuration in 'config.xlsx' file
* run the 'run.bat' file
* you can see the outut report generated in the user configured dump folder

## Configuration
### API fetch configuration
This configuration is defined in the config sheet of config.xlsx file
The description of configuration parameters is as follows
* dummyFetchFlag: If its value is 1, dummy data will be dumped
* host: ip address of api host (example: '10.5.10.6')
* port: port of the data api service (example: 80)
* path: path of the data fetch api (example: '/path/to/api')
* username: username for data api access (example: 'uname')
* password: password for data api access (example: 'pass')
* refMeasId: reference measurement id for data fetch (example: 100)

### Dumping configuration
This configuration is defined in the config sheet of config.xlsx file
* dumpFolder: folder path at which the report is to be dumped (example: 'D:\dumps\pmudata')
* filenamePrefix: prefix of the report filename (example: 'pmu_report_')

## Data fetch start and end times configuration
This configuration is defined in the config sheet of config.xlsx file
* absoluteStartTime: Date time of start time
* varStartYears: if this value is non-empty the years component of start time will be dynamic (example: -1)
* varStartMonths: if this value is non-empty the months component of start time will be dynamic (example: -1)
* varStartDays: if this value is non-empty the days component of start time will be dynamic (example: -1)
* varStartHours: if this value is non-empty the hours component of start time will be dynamic (example: -1)
* varStartMinutes: if this value is non-empty the minutes component of start time will be dynamic (example: -1)
* varStartSeconds: if this value is non-empty the seconds component of start time will be dynamic (example: -1)
* absoluteEndTime: dt.datetime
* varEndYears: if this value is non-empty the years component of end time will be dynamic (example: -1)
* varEndMonths: if this value is non-empty the months component of end time will be dynamic (example: -1)
* varEndDays: if this value is non-empty the days component of end time will be dynamic (example: -1)
* varEndHours: if this value is non-empty the hours component of end time will be dynamic (example: -1)
* varEndMinutes: if this value is non-empty the minutes component of end time will be dynamic (example: -1)
* varEndSeconds: if this value is non-empty the seconds component of end time will be dynamic (example: -1)

## data resampling configuration
This configuration is defined in the config sheet of config.xlsx file

Data from API contains 25 samples in 1 second duration. We can resample data using the following configuration
* resampleFrequency: any one of the below options can be used
    * 's' - data resolution will be 1 second
    * 'm' - data resolution will be 1 minute
    * 'b' - data resolution will be 1 time block (15 mins)
    * 'h' - data resolution will be 1 hour
    * 'd' - data resolution will be 1 day
    * If none of the above option is mentioned, no resampling will be performed
* sampleAggregationStrategy: any one of the below options can be used
    * 'raw' - no resampling will be performed
    * 'snap' - first valid sample of the resampling window will be taken for data aggregation
    * 'average' - average of valid samples of the resampling window will be taken for data aggregation

## fetch window configuration
This configuration is defined in the config sheet of config.xlsx file

You can fetch data in time windows using the below configuration
* fetchWindowDays: (example: 1)
* fetchWindowHours: (example: 1)
* fetchWindowMinutes: (example: 1)
* fetchWindowSeconds: (example: 1)
If fetch window is 0, or more than (endTime-startTime), then data will not be fetched in time windows

## Notable features of this script
* If data of some signals / all signals is completely absent / intermittent, the script will not crash, instead missing samples will be dumped as empty cells in the output report. Hence the data of all signals is time aligned even if data is completely / partially unavailable
* Only 'GOOD' quality data is dumped in the report. Other quality data is dumped as blank cells in the output report
* The dynamic start time and end time configuration provides peridic data dumping capability to this script