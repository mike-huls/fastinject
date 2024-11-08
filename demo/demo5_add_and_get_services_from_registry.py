from typing import List, Dict

from src.fastinject import inject, get_default_registry

""" 
Instead of declaratively marking Services as "injectable", it's also possible to do so imperatively. 
The code below allows you to add Services on the fly
1. Get the default registry
2. Add one or more services to the registry 

"""


class ApiClient:
    def __init__(self) -> None:
        pass

    def get_users(self) -> List[Dict]:
        """retrieves users from the database"""
        return [{"id": 1, "name": "mike"}]


@inject()
def my_function(api_client: ApiClient):
    print(f"Retrieving users with api-client {id(api_client)}: {api_client.get_users()}")


if __name__ == "__main__":
    reg = get_default_registry()
    reg.add_service(ApiClient)
    my_function()

    api_client: ApiClient = reg.get(ApiClient)
    print(api_client.get_users())
