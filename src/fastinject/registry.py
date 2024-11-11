from typing import Any, Type, Union, Callable, List, Optional  # , Self,  Iterable

from injector import Injector, Binder
from injector import Scope, ScopeDecorator, Module
from injector import T

from . import logger
from .service_config import ServiceConfig


# _InstallableModuleType = Union[Callable[['XBinder'], None], 'Module', Type['Module']]
_InstallableModuleType = Union["Service", Type["Service"]]


# class XBinder(Binder):
#     def __init__(self, parent: Binder) -> None:
#         self._parent = parent
#
#     def bind(
#         self,
#         interface: Type[T],
#         to: Union[None, T, Callable[..., T], Provider[T]] = None,
#         scope: Union[None, Type["Scope"], "ScopeDecorator"] = None,
#     ) -> None:
#         self._parent.bind(interface, to, scope)


class Registry:
    """_setup_functions contain functions that let us imperatively register a service within a dependency injection Registry.
    It dynamically binds a configuration object to the registry without using decorators, allowing for on-the-fly service binding
    """

    _auto_bind: bool
    _services: List[Type]
    _service_configs: List[ServiceConfig]
    _setup_functions: List[Callable[[Binder], None]]

    def __init__(
        self,
        service_configs: Optional[List[_InstallableModuleType]] = None,
        services: Optional[List[_InstallableModuleType]] = None,
        auto_bind: bool = False,
    ) -> None:
        """
        auto_bind: bool : if True; will automatically resolve types that it can construct. Looks in all functions decorated with @provider.

        """
        self._auto_bind = auto_bind
        self._service_configs: List[ServiceConfig] = []
        self._services: List[Type] = []
        self._setup_functions: List[Callable[[Binder], None]] = []
        for service_config in service_configs or []:
            self.add_service_config(service_config=service_config)
        for service in services or []:
            self.add_service(service=service)
        self.__build()

    def __str__(self) -> str:
        return f"<Registry ({len(self._service_configs)} service configs, {len(self._services)} services)>"

    def __repr__(self) -> str:
        return self.__str__()

    def add_service(self, service: Type, scope: Optional[Scope] = None) -> "Registry":
        def _setup_function(binder: Binder):
            binder.bind(service, to=service, scope=scope)

        self._setup_functions.append(_setup_function)
        self._services.append(service)
        self.__build()
        return self

    def add_service_config(self, service_config: _InstallableModuleType) -> "Registry":
        self._service_configs.append(service_config)
        self.__build()
        return self

    # def bind(
    #     self,
    #     interface: Type[T],
    #     to: Union[None, T, Callable[..., T], Provider[T]] = None,
    #     scope: Union[None, Type["Scope"], "ScopeDecorator"] = None,
    # ) -> "T":
    #     return self.add_setup(lambda binder: binder.bind(interface, to, scope))

    def __build(self) -> "Registry":
        def configure(binder: Binder):
            for fn in self._setup_functions:
                fn(binder)

        # setup:ParentListList = [configure]
        setup: List[Callable] = [configure]
        for m in self._service_configs:
            setup.append(m)

        # self._injector = Injector([configure_for_testing, di.TestModule()])
        self._injector = Injector(setup, auto_bind=self._auto_bind)
        set_default_registry(registry=self)
        return self
        # result = RegistryDEPRECATED(self._injector)
        # for modifier in self._modifiers:
        #     # if self._modifier:
        #     modifier(result, self._injector)

        # auto register the first registry as default registry
        # if get_default_registry() is None:
        #     set_default_registry(result)
        # return result

    def get(self, interface: Type[T], scope: Union[ScopeDecorator, Type[Scope], None] = None) -> T:
        """
        Gets an instance of T and if it is decorated with @inject or any of the __init__ arguments are wrapped with Inject[...] the dependencies will be injected
        """
        try:
            return self._injector.get(interface=interface, scope=scope)
        except Exception as e:
            print(f"exception::::: {type(e)} {e}")
            logger.warning(f"Failed to get instance of {interface} with scope {scope}: {e}")
            return None

    def call_with_injection(
        self,
        callable: Callable[..., T],
        self_: Any = None,
        args: Optional[Any] = None,
        kwargs: Optional[Any] = None,
    ) -> T:
        """
        Calls the function and injects the parameters if the function is decorated with @inject or any of the arguments are wrapped with Inject[..]
        """
        args = args if args is not None else ()
        kwargs = kwargs if kwargs is not None else {}
        return self._injector.call_with_injection(callable, self_, args, kwargs)


__default_registry: Optional[Registry] = None


def set_default_registry(registry: Registry):
    global __default_registry
    __default_registry = registry


def get_default_registry() -> Registry:
    if __default_registry is None:
        set_default_registry(Registry())
    return __default_registry
