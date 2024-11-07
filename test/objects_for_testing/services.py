import time


class MyDatabaseConfig:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    @property
    def connection_string(self) -> str:
        return self._connection_string


class TimeStamp:
    init_time: float
    def __init__(self) -> None:
        self.init_time = time.time()

    def time_passed(self) -> float:
        return time.time() - self.init_time

class TimeStampLogger:
    timestamp:TimeStamp

    def __init__(self, timestamp: TimeStamp) -> None:
        self.timestamp = timestamp
