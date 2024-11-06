class MyDatabaseConfig:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    @property
    def connection_string(self) -> str:
        return self._connection_string
