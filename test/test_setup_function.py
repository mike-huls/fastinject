# from src.injectr import singleton, Registry
#
# from test.objects_for_testing import services
#
#
# def test_can_register_service_on_registry_imperatively():
#     """ For binding a service to a module on the fly """
#     def configure_for_testing(binder):
#         """ Puts a service in a registry without the decorators """
#         configuration = services.MyDatabaseConfig("file:memdb1?mode=memory&cache=shared")
#         binder.bind(services.MyDatabaseConfig, to=configuration, scope=singleton)
#
#     # Create empty registry; no modules added
#     registry = Registry()
#     assert registry._modules == []
#     registry.add_setup_function(configure_for_testing)
#
#     service: services.MyDatabaseConfig = registry.get(services.MyDatabaseConfig)
#     assert service.connection_string == "file:memdb1?mode=memory&cache=shared"
#
#
