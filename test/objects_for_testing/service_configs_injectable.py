import logging

from src.fastinject import singleton, provider, injectable
from src.fastinject.service_config import ServiceConfig
from test.objects_for_testing.services import DatabaseConfig, TimeStamp, TimeStampLogger


# ConnectionString = NewType("ConnectionString", str)


@injectable()
class ModuleDatabaseLogging(ServiceConfig):
    @singleton
    @provider
    def provide_config(self) -> DatabaseConfig:
        return DatabaseConfig(connection_string="file:memdb1?mode=memory&cache=shared3")

    @singleton
    @provider
    def provide_logger(self) -> logging.Logger:
        return logging.getLogger("testing")


@injectable()
class ModuleLogging(ServiceConfig):
    @singleton
    @provider
    def provide_logger(self) -> logging.Logger:
        return logging.getLogger("testing")


@injectable()
class ModuleDatabase(ServiceConfig):
    @singleton
    @provider
    def provide_config(self) -> DatabaseConfig:
        return DatabaseConfig(connection_string="file:memdb1?mode=memory&cache=shared3")


@injectable()
class ModuleTimestamper(ServiceConfig):
    @provider
    def provide_timestamper(self) -> TimeStamp:
        return TimeStamp()


@injectable()
class ModuleTimestamperWeirdImport(ServiceConfig):
    @singleton
    @provider
    def provide_timestamper(self) -> TimeStamp:
        return TimeStamp()


@injectable()
class ModuleNestedDependenciesSimple(ServiceConfig):
    @singleton
    @provider
    def provide_timestamper(self) -> TimeStamp:
        return TimeStamp()

    @provider
    def provide_timestamplogger(self) -> TimeStampLogger:
        return TimeStampLogger(timestamp=self.provide_timestamper())


@injectable()
class ModuleWithTimeStampButNoNoopService(ServiceConfig):
    @singleton
    @provider
    def provide_timestamper(self) -> TimeStamp:
        return TimeStamp()
