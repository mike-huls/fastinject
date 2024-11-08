import datetime
import time

from src.injectr import inject, injectable


@injectable()
class TimeStamp:
    ts: float

    def __init__(self) -> None:
        self.set()

    def set(self):
        self.ts = time.time()

    @property
    def datetime_str(self) -> str:
        return datetime.datetime.fromtimestamp(self.ts).strftime("%Y-%m-%d %H:%M:%S")


class NotInjectedService:
    def __init__(self):
        pass
