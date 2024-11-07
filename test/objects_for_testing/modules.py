import logging

from src.injectr import singleton, provider, Module
from test.objects_for_testing import services
from test.objects_for_testing.services import MyDatabaseConfig, TimeStamp


# ConnectionString = NewType("ConnectionString", str)


class ModuleDatabaseLogging(Module):
    @singleton
    @provider
    def provide_config(self) -> MyDatabaseConfig:
        return MyDatabaseConfig(connection_string="file:memdb1?mode=memory&cache=shared3")

    @singleton
    @provider
    def provide_logger(self) -> logging.Logger:
        return logging.getLogger("testing")


class ModuleLogging(Module):
    @singleton
    @provider
    def provide_logger(self) -> logging.Logger:
        return logging.getLogger("testing")


class ModuleDatabase(Module):
    @singleton
    @provider
    def provide_config(self) -> MyDatabaseConfig:
        return MyDatabaseConfig(connection_string="file:memdb1?mode=memory&cache=shared3")

class ModuleTimestamper(Module):
    @provider
    def provide_timestamper(self) -> TimeStamp:
        return TimeStamp()


class ModuleTimestamperWeirdImport(Module):
    @singleton
    @provider
    def provide_timestamper(self) -> services.TimeStamp:
        return services.TimeStamp()


class ModuleNestedDependenciesSimple(Module):

    @singleton
    @provider
    def provide_timestamper(self) -> services.TimeStamp:
        return services.TimeStamp()

    @provider
    def provide_timestamplogger(self) -> services.TimeStampLogger:
        return services.TimeStampLogger(timestamp=self.provide_timestamper())

