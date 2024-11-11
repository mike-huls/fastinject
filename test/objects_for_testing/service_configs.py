import logging

from src.fastinject import singleton, provider
from src.fastinject.service_config import ServiceConfig
from test.objects_for_testing import services
from test.objects_for_testing.services import DatabaseConfig, TimeStamp


# ConnectionString = NewType("ConnectionString", str)


class SCDatabaseLogging(ServiceConfig):
    @provider
    def provide_config(self) -> DatabaseConfig:
        return DatabaseConfig(connection_string="file:memdb1?mode=memory&cache=shared3")

    @provider
    def provide_logger(self) -> logging.Logger:
        return logging.getLogger("testing")


class SCLogging(ServiceConfig):
    @provider
    def provide_logger(self) -> logging.Logger:
        return logging.getLogger("testing")


class SCDatabase(ServiceConfig):
    @provider
    def provide_config(self) -> DatabaseConfig:
        return DatabaseConfig(connection_string="file:memdb1?mode=memory&cache=shared3")


class SCTimestamper(ServiceConfig):
    @provider
    def provide_timestamper(self) -> TimeStamp:
        return TimeStamp()


class SCTimestamperWeirdImport(ServiceConfig):
    @provider
    def provide_timestamper(self) -> services.TimeStamp:
        return services.TimeStamp()


class SCNestedDependenciesSimple(ServiceConfig):
    @provider
    def provide_timestamper(self) -> services.TimeStamp:
        return services.TimeStamp()

    @provider
    def provide_timestamplogger(self) -> services.TimeStampLogger:
        return services.TimeStampLogger(timestamp=self.provide_timestamper())


class SCDatabaseInitFails(ServiceConfig):
    @provider
    def provide_db_config(self) -> services.DatabaseConfig:
        return services.DatabaseConfig(connection_string="my_db_constring")

    @provider
    def provide_db_connection(self) -> services.DatabaseConnection:
        # FAIL:
        print(1 / 0)
        return services.DatabaseConnection(dbconfig=self.provide_db_config)
