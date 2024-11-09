import datetime
import logging
import time
import uuid

from src.fastinject import singleton, provider, inject, logger, get_default_registry, injectable, ServiceConfig


class TimeStamp:
    init_time: float

    def __init__(self) -> None:
        self.init_time = time.time()

    def to_string(self) -> str:
        return datetime.datetime.fromtimestamp(self.init_time).strftime("%Y-%m-%d %H:%M:%S")


@injectable()
class IdGenerator:
    the_id: str

    def __init__(self) -> None:
        self.the_id = str(uuid.uuid4())


@injectable()
class MyConfig(ServiceConfig):
    @provider
    def provide_timestamper(self) -> TimeStamp:
        return TimeStamp()

    @provider
    def provide_logger(self) -> logging.Logger:
        return logging.getLogger("LoggerName")


# registry = Registry(modules=[ServiceConfig])


@inject()
def function_with_injection(_logger: logging.Logger, ts: TimeStamp, idgen: IdGenerator):
    _logger.setLevel(level=logging.DEBUG)
    _logger.warning(f"Hello from within the function! Time: {ts.to_string()}")
    _logger.warning(f"injected id: {ts.to_string()}")
    _logger.warning(f"idgen: {idgen}")
    _logger.warning(f"idgen: {idgen.the_id}")


@inject()
def function_with_injection_simple(idgen: IdGenerator):
    print(f"idgen: {idgen.the_id}")


if __name__ == "__main__":
    logger.setLevel(level=logging.DEBUG)
    registry = get_default_registry()
    print(registry._modules)
    # registry.add_module(module=ServiceConfig)

    function_with_injection()
    function_with_injection_simple()
    print(get_default_registry()._modules)
    print(id(get_default_registry().get(TimeStamp)))
    print(id(get_default_registry().get(TimeStamp)))
    print(id(get_default_registry().get(IdGenerator)))
    print(id(get_default_registry().get(IdGenerator)))
