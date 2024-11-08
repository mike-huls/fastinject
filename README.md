#FastInject: easy Python dependency injection

![coverage](https://img.shields.io/codecov/c/github/mike-huls/fastinject)
![Tests](https://github.com/mike-huls/fastinject/actions/workflows/tests.yml/badge.svg)
![version](https://img.shields.io/pypi/v/fastinject?color=%2334D058&label=pypi%20package)
![dependencies](https://img.shields.io/librariesio/release/pypi/fastinject)
![PyPI Downloads](https://img.shields.io/pypi/dm/fastinject.svg?label=PyPI%20downloads)
![versions](https://img.shields.io/pypi/pyversions/fastinject.svg?color=%2334D058)
<br>
![tweet](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fmike-huls%2Ffastinject) ![xfollow](https://img.shields.io/twitter/follow/mike_huls?style=social)

[//]: # (|         |                                                                                                                                                                                                                                                                                                                                                               |)
[//]: # (|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|)
[//]: # (| Testing | ![coverage]&#40;https://img.shields.io/codecov/c/github/mike-huls/cachr&#41;                                                                                                                                                                                                                                                                                          |)
[//]: # (| Package | [![PyPI Latest Release]&#40;https://img.shields.io/pypi/v/cachr.svg&#41;]&#40;https://pypi.org/project/cachr/&#41; [![PyPI Downloads]&#40;https://img.shields.io/pypi/dm/cachr.svg?label=PyPI%20downloads&#41;]&#40;https://pypistats.org/packages/cachr&#41; <br/>![status]&#40;https://img.shields.io/pypi/status/cachr&#41; ![dependencies]&#40;https://img.shields.io/librariesio/release/pypi/cachr&#41; |)
[//]: # (| Meta    | ![GitHub License]&#40;https://img.shields.io/github/license/mike-huls/cachr&#41; ![implementation]&#40;https://img.shields.io/pypi/implementation/cachr&#41;  ![versions]&#40;https://img.shields.io/pypi/pyversions/cachr&#41;                                                                                                                                                       |)
[//]: # (| Social  | ![tweet]&#40;https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fmike-huls%2Fcachr&#41; ![xfollow]&#40;https://img.shields.io/twitter/follow/mike_huls?style=social&#41;                                                                                                                                                                           | )

**FastInject** provides easy dependency injection for Python that makes you code decoupled, testable, uncomplicated and more readable.
Decorate your services with the `@injectable` decorator and decorate your function with `@inject`. Done! 
Your function will now be injected with instances of the required service.
```shell
pip install fastinject
```

## Table of Contents
- [Main Features](#main-features)
- [Usage Example](#Usage-example)
- [Installation](#Installation)
- [Dependencies](#Dependencies)
- [License](#license)
- [Documentation](#documentation)
- [Development](#development)
- [Contributing to Cachr](#Development)
<hr>

## Main Features
- 🐍 Pure Python
- 🤸 Flexible
- 🎩 Tailor-made for your app
- 👨‍🎨 Easy to use with decorators

## How to
Injecting services
- [Register and inject a single service](demo/demo1_inject_single_service.py).
- [Register and inject a single service as a singleton](demo/demo2_inject_single_service_singleton.py).

Inject services that depend on one another
- [ServiceConfig: Register multiple dependencies for injection](demo/demo3_inject_service_config.py).
- [ServiceConfig: Register nested dependencies for injection](demo/demo4_inject_service_config_nested_dependencies.py).

Use the service registy imperatively to get and set dependencies on the fly
- [Declare service to be injectable imperatively](demo/demo5_add_and_get_services_from_registry.py).
- [Declare service to be injectable and declare function to inject imperatively](demo/demo6_add_and_get_service_config_imperatively.py).

Use multiple registries?
- [Use multiple regisries](demo/demo7_multiple_registries.py)
<hr>

## Usage Example
Below details a 

#### Step 1: Declare service to be injectable
We have a service that we want to inject, so we mark it `injectable` with a decorator:
```python
import time, datetime
from fastinject import injectable

@injectable()           # <-- Just add this decorator to declare the TimeStamp service to be injectable
class TimeStamp:
    ts: float

    def __init__(self) -> None:
        self.ts = time.time()

    @property
    def datetime_str(self) -> str:
        return datetime.datetime.fromtimestamp(self.ts).strftime("%Y-%m-%d %H:%M:%S")
```

Step 2: Use the service in a function that is injected in
```python
from fastinject import inject

@inject()               # <-- This decorator will inject required services in this function
def function_with_injection(ts: TimeStamp):
    print(f"In the injected function, the current time is {ts.datetime_str}.")

if __name__ == "__main__":
    function_with_injection()
```



## Installation
```sh
pip install fastinject
```
The source code is currently hosted on GitHub at:
https://github.com/mike-huls/fastinject

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/fastinject).

## Dependencies
FastInject has one major dependency: `injector`. FastInject aims to build on `injector` by making it easier to use.

## License
[MIT](LICENSE.txt)

## Documentation
🔨 Under construction

## Development
Find the changelog and list of upcoming features [here](doc/CHANGELOG.md).
<br>
**Contributions** are always welcome; feel free to submit bug reports, bug fixes, feature requests, documentation improvements or enhancements!

<hr>

[Go to Top](#table-of-contents)
