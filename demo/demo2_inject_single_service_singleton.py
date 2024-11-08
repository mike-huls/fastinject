from typing import Dict, List

from src.fastinject import inject, injectable, singleton

"""
You can mark a servise as "singleton" so that no more than one instance gets created throughout the app.
The example below details an ApiClient; we only need one of those throughout the app, no need for more instances than one.

OUTPUT:
Notice the same ids
fn1: Retrieving users with api-client 2943721761472: [{'id': 1, 'name': 'mike'}]
fn2: Retrieving users with api-client 2943721761472: [{'id': 1, 'name': 'mike'}]


Note: only works with services that don't need arguments to initialize with. Otherwise use the ServiceConfig (demo2)
"""


@injectable(scope=singleton)
class ApiClient:
    def __init__(self) -> None:
        pass

    def get_users(self) -> List[Dict]:
        """retrieves users from the database"""
        return [{"id": 1, "name": "mike"}]


@inject()
def function_1(api_client: ApiClient):
    print(f"fn1: Retrieving users with api-client {id(api_client)}: {api_client.get_users()}")


@inject()
def function_2(api_client: ApiClient):
    print(f"fn2: Retrieving users with api-client {id(api_client)}: {api_client.get_users()}")


# todo : test singleton

if __name__ == "__main__":
    function_1()
    function_2()
