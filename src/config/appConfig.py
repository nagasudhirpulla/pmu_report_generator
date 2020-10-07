import pandas as pd
from src.typeDefs.appConfig import IAppConfig
import json


def getConfig(configFilename='config.json') -> IAppConfig:
    """Get the application config from config.json file

    Args:
        configFilename (str, optional): path of config file. Defaults to 'config.json'.

    Raises:
        Exception: throws exception if not OK

    Returns:
        IAppConfig: The application configuration as a dictionary
    """
    with open(configFilename, "r") as configFile:
        configDict = json.load(configFile)
        return configDict
    raise Exception("Unable to read config file")
