import logging
import time
from functools import wraps

from src.fastinject import provider
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

# Needed to test that only methods get validated that are decorated with @provider
def timer(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    start = time.perf_counter()

    # Call the actual function
    res = func(*args, **kwargs)

    duration = time.perf_counter() - start
    print(f'[{wrapper.__name__}] took {duration * 1000} ms')
    return res
  return wrapper

class SCDatabaseInitFails(ServiceConfig):
    @provider
    def provide_db_config(self) -> services.DatabaseConfig:
        return services.DatabaseConfig(connection_string="my_db_constring")

    @provider
    def provide_db_connection(self) -> services.DatabaseConnection:
        # FAIL:
        print(1 / 0)
        return services.DatabaseConnection(dbconfig=self.provide_db_config)

    @timer
    def decorated_with_my_thing(self) -> services.TimeStampLogger:
        pass
