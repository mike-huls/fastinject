import datetime
import time
from typing import Any, Optional

from src.injectr import inject, injectable


@injectable()
class LabelPrinter:
    label:Optional[str]
    def __init__(self, label:Optional[Any]=None) -> None:
        self.label = label if label is not None else None
    def print(self, *args):
        msg = " ".join(args)
        print(f"{self.label}: {msg}")





@inject()
def function_with_injection(lp: LabelPrinter):
    lp.print("hello from the injected function")



if __name__ == "__main__":
    function_with_injection()

