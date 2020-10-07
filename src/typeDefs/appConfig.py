from typing import TypedDict


class IAppConfig(TypedDict):
    host: str
    port: int
    path: str
    username: str
    password: str
    refMeasId: int
