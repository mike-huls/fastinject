import datetime
import logging
import time

from src.injectr import Registry, Module, singleton, provider, inject_from, inject, logger


# Services
class TimeStamp:
    init_time: float
    def __init__(self) -> None:
        self.init_time = time.time()
    def to_string(self) -> str:
        return datetime.datetime.fromtimestamp(self.init_time).strftime("%Y-%m-%d %H:%M:%S")


class ServiceConfig(Module):
    @singleton
    @provider
    def provide_timestamper(self) -> TimeStamp:
        return TimeStamp()

    @singleton
    @provider
    def provide_logger(self) -> logging.Logger:
        return logging.getLogger("LoggerName")


registry = Registry(modules=[ServiceConfig])


@inject_from(registry=registry)
def function_with_injection(_logger: logging.Logger, ts: TimeStamp):
    _logger.setLevel(level=logging.DEBUG)
    _logger.warning(f"Hello from within the function! Time: {ts.to_string()}")


if __name__ == "__main__":
    logger.setLevel(level=logging.DEBUG)
    function_with_injection()