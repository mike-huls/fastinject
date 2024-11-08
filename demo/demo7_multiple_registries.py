import datetime
import time
from typing import Any, Optional
from src.injectr import inject, injectable, ServiceConfig, singleton, provider, get_default_registry, Registry

""" 
In some cases multiple registries may be required. 
This file demonstrates how to create two distinct registries and inject from those registries
We want TimeStamp in registry1 and MyServiceConfig (which contains DatabaseConnection and AppConfiguration) in regsitry2
"""


# region Services
class TimeStamp:
    init_time: float

    def __init__(self) -> None:
        self.init_time = time.time()

    def to_string(self) -> str:
        return datetime.datetime.fromtimestamp(self.init_time).strftime("%Y-%m-%d %H:%M:%S")


class AppConfiguration:
    connection_string: str

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string


class DatabaseConnection:
    database_engine: str

    def __init__(self, connection_string: str):
        self.database_engine = f"DBCON - {connection_string}"


# endregion


class MyServiceConfig(ServiceConfig):
    @singleton
    @provider
    def provide_app_config(self) -> AppConfiguration:
        return AppConfiguration("my_db_config_string")

    @singleton
    @provider
    def provide_database_connection(self) -> DatabaseConnection:
        return DatabaseConnection(connection_string=self.provide_app_config().connection_string)


@inject()
def function_with_injection(dbcon: DatabaseConnection):
    print(f"working with dbcon that uses this engine: '{dbcon.database_engine}'")


def main():
    registry1 = Registry(services=[TimeStamp])
    registry2 = Registry(service_configs=[MyServiceConfig])

    assert registry1.get(TimeStamp) is not None
    assert registry2.get(DatabaseConnection) is not None

    assert registry1.get(DatabaseConnection) is None
    assert registry2.get(TimeStamp) is None


if __name__ == "__main__":
    main()
