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




@inject()
def function_with_injection(ts: TimeStamp):
    print(f"In the injected function, the current time is {ts.datetime_str}.")

# todo : test singleton

if __name__ == "__main__":
    function_with_injection()

