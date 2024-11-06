import logging

from src.injectr import singleton, provider, XModule
from test.objects_for_testing.services import MyDatabaseConfig


# ConnectionString = NewType("ConnectionString", str)


class RegDatabaseLogging(XModule):
    @singleton
    @provider
    def provide_config(self) -> MyDatabaseConfig:
        return MyDatabaseConfig(connection_string="file:memdb1?mode=memory&cache=shared3")

    @singleton
    @provider
    def provide_logger(self) -> logging.Logger:
        return logging.getLogger("testing")


class RegLogging(XModule):
    @singleton
    @provider
    def provide_logger(self) -> logging.Logger:
        return logging.getLogger("testing")


class RegDatabase(XModule):
    @singleton
    @provider
    def provide_config(self) -> MyDatabaseConfig:
        return MyDatabaseConfig(connection_string="file:memdb1?mode=memory&cache=shared3")
