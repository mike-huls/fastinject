from src.fastinject import inject, ServiceConfig, singleton, provider, get_default_registry

""" 
Instead of declaratively marking ServiceConfigs as "injectable", it's also possible to do so imperatively. 
The code below allows you to add ServiceConfigs on the fly
"""


# region Services
class AppConfiguration:
    connection_string: str

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string


class DatabaseConnection:
    database_engine: str

    def __init__(self, connection_string: str):
        self.database_engine = f"DBCON - {connection_string}"


# endregion


class MyServiceConfig(ServiceConfig):
    @singleton
    @provider
    def provide_app_config(self) -> AppConfiguration:
        return AppConfiguration("my_db_config_string")

    @singleton
    @provider
    def provide_database_connection(self) -> DatabaseConnection:
        return DatabaseConnection(connection_string=self.provide_app_config().connection_string)


@inject()
def function_with_injection(dbcon: DatabaseConnection):
    print(f"working with dbcon that uses this engine: '{dbcon.database_engine}'")


if __name__ == "__main__":
    reg = get_default_registry()
    reg.add_service_config(MyServiceConfig)
    function_with_injection()

    dbcon: DatabaseConnection = reg.get(DatabaseConnection)
    print(f"dbengine: {dbcon.database_engine}")
