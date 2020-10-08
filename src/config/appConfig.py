import pandas as pd
from src.typeDefs.appConfig import IAppConfig
from src.typeDefs.fetchPnt import FetchPnt
import json
from typing import List


def getConfig(configFilename='config.xlsx', sheetName='config') -> IAppConfig:
    """Get the application config from config.xlsx file

    Args:
        configFilename (str, optional): path of config file. Defaults to 'config.xlsx'.

    Raises:
        Exception: throws exception if not OK

    Returns:
        IAppConfig: The application configuration as a dictionary
    """
    df = pd.read_excel(configFilename, sheet_name=sheetName,
                       header=None, index_col=0)
    configDict: IAppConfig = df[1].to_dict()
    return configDict


def getFetchPnts(configFilename='config.xlsx', sheetName='pnts') -> List[FetchPnt]:
    """Get the list of points to be fetched from config file

    Args:
        configFilename (str, optional): The excel file from which config is to extracted. Defaults to 'config.xlsx'.
        sheetName (str, optional): sheet name from which points are to be extracted. Defaults to 'pnts'.

    Returns:
        List[FetchPnt]: [description]
    """
    df = pd.read_excel(configFilename, sheet_name=sheetName)
    pnts: List[FetchPnt] = df.to_dict('records')
    return pnts
