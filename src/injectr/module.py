import inspect
from functools import wraps
from typing import Callable, Optional

from typing import NewType
from injector import Module

# from injector import Module, provider, Injector, inject
from injector import singleton, threadlocal, noscope


# simple wrapper around module


# TODO MH: rename; also rename in injection.py l.13
class XModule(Module):
    pass


# example to create wrap it in a new type that acts like a subclass
# Module2 = NewType("Module2", Module)
# module = Module2(Module())
