# FastInject: easy Python dependency injection

[![coverage](https://img.shields.io/codecov/c/github/mike-huls/fastinject)](https://codecov.io/gh/mike-huls/fastinject)
[![Tests](https://github.com/mike-huls/fastinject/actions/workflows/tests.yml/badge.svg)](https://github.com/mike-huls/fastinject/actions/workflows/tests.yml)
[![version](https://img.shields.io/pypi/v/fastinject?color=%2334D058&label=pypi%20package)](https://pypi.org/project/fastinject)
[![dependencies](https://img.shields.io/librariesio/release/pypi/fastinject)](https://pypi.org/project/fastinject)
[![PyPI Downloads](https://img.shields.io/pypi/dm/fastinject.svg?label=PyPI%20downloads)](https://pypistats.org/packages/fastinject)
[![versions](https://img.shields.io/pypi/pyversions/fastinject.svg?color=%2334D058)](https://pypi.org/project/fastinject)
<br>
[![tweet](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fmike-huls%2Ffastinject)](https://twitter.com/intent/tweet?text=Check%20this%20out:&url=https%3A%2F%2Fgithub.com%2Fmike-huls%2Ffastinject) 
[![xfollow](https://img.shields.io/twitter/follow/mike_huls)](https://twitter.com/intent/follow?screen_name=mike_huls)


**FastInject** provides lazy dependency injection for Python that makes your code decoupled, testable, uncomplicated and more readable.
Decorate your services with the `@injectable` decorator and decorate your function with `@inject`. Done! 
Your function will now be injected with instances of the required service.
```shell
pip install fastinject
```

## Table of Contents
- [Main Features](#main-features)
- [Usage Example](#Usage-example)
- [How to](#How-to)
- [Installation](#Installation)
- [Dependencies](#Dependencies)
- [License](#license)
- [Documentation](#documentation)
- [Development](#development)
- [Contributing to Cachr](#Development)
<hr>

## Main Features
- 🦥 Lazily declare and register your dependencies
- 🐇 Eagerly validate your dependencies
- 🤸 Flexible
- 🎩 Tailor-made for your app
- 👨‍🎨 Easy to use with decorators
<hr>

## Usage Example
Below details a minimal use case 

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

Step 3: Optinonally validate that all injected services can be injected:
```python
from fastinject import get_default_registry

if __name__ == "__main__":
    registry = get_default_registry()

    # Validate
    registry.validate()
    function_with_injection()

```
<hr>

## How to use
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
- [Use multiple registries](demo/demo7_multiple_registries.py)

Register similar services?
- [Register multiple services of the same type?](demo/demo8_register_multiple_instances_of_the_same_type.py)

Validation
- [Validated registered services?](demo/demo9_eagerly_validate.py)

<hr>


## Installation
```sh
pip install fastinject
```
The source code is currently hosted on GitHub at:
https://github.com/mike-huls/fastinject

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/fastinject).

<hr>

## Dependencies
FastInject is built on `injector`, aiming to provide additional features and ease-of-use.

<hr>

## License
[MIT](LICENSE.txt)

<hr>

## Development
Find the changelog and list of upcoming features [here](CHANGELOG.md).
<br>
**Contributions** are always welcome; feel free to submit bug reports, bug fixes, feature requests, documentation improvements or enhancements!

<hr>

[Go to Top](#table-of-contents)
