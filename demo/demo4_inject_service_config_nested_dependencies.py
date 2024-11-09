from src.fastinject import inject, injectable, ServiceConfig, singleton, provider

""" 
If you have services that need arguments to be inialized or services that are dependent on other services you need the ServiceConfig.
This is a class that specifies how injectable services are initialized. 

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


@injectable()
class MyServiceConfig(ServiceConfig):
    @provider
    def provide_app_config(self) -> AppConfiguration:
        return AppConfiguration("my_db_config_string")

    @provider
    def provide_database_connection(self) -> DatabaseConnection:
        return DatabaseConnection(connection_string=self.provide_app_config().connection_string)


@inject()
def function_with_injection(dbcon: DatabaseConnection):
    print(f"working with dbcon that uses this engine: '{dbcon.database_engine}'")


if __name__ == "__main__":
    function_with_injection()
