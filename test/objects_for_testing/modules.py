import logging

from src.injectr import singleton, provider, Module
from test.objects_for_testing import services
from test.objects_for_testing.services import MyDatabaseConfig, TimeStamp


# ConnectionString = NewType("ConnectionString", str)


class RegDatabaseLogging(Module):
    @singleton
    @provider
    def provide_config(self) -> MyDatabaseConfig:
        return MyDatabaseConfig(connection_string="file:memdb1?mode=memory&cache=shared3")

    @singleton
    @provider
    def provide_logger(self) -> logging.Logger:
        return logging.getLogger("testing")


class RegLogging(Module):
    @singleton
    @provider
    def provide_logger(self) -> logging.Logger:
        return logging.getLogger("testing")


class RegDatabase(Module):
    @singleton
    @provider
    def provide_config(self) -> MyDatabaseConfig:
        return MyDatabaseConfig(connection_string="file:memdb1?mode=memory&cache=shared3")

class RegTimestamper(Module):
    @singleton
    @provider
    def provide_timestamper(self) -> TimeStamp:
        return TimeStamp()


class RegTimestamperWeirdImport(Module):
    @singleton
    @provider
    def provide_timestamper(self) -> services.TimeStamp:
        return services.TimeStamp()
