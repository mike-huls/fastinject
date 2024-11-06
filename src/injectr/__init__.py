# Import classes / functions / modules here to make them available in your package
__version__ = "0.1.0.30"
__last_build_datetime__ = "2024-05-01 11:46:16"
__last_publish_version__ = "0.1.0.29"
__last_publish_datetime__ = "2024-04-10 11:28:55"

from .module import XModule
from .helpers import *
from .default_registry import Registry
from .injection import RegistryBuilder, Binder
from .decorators import inject_services, get_default_registry, set_default_registry

# from injector import Module, provider, Injector, inject
from injector import provider, inject, Inject
from injector import singleton, threadlocal as scope_threadlocal, noscope as scope_none

# .fastapi moved to injectr
# dont'export it here so we can move it to a separate package later
# from .fastapi import FastApiRegistryBuilder
