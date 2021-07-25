# dataclasses-settings

Oversimplified decorator for settings management (via environment variables) with built in dataclasses superpowers.

[![PyPI version](https://badge.fury.io/py/dataclass-settings.svg)](https://badge.fury.io/py/dataclass-settings)
[![Test](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Installation

Install using `pip install git+https://github.com/shpaker/dataclasses-settings.git`.

## Usage

1. Specify environments variables:

    ```shell
    export APP_PORT=8080
    export APP_DEBUG=yes
    export APP_RULESET_PATH=./ruleset.yaml
    ```

1. Define class for settings with defaults values:

    ```python
    from pathlib import Path

    from dataclasses_settings import dataclass_settings

    @dataclass_settings(prefix="app_", frozen=True)
    class Settings:
        port: int
        debug: bool = False
        ruleset_path: Path = None
    ```

1. Check result:

    ```python
    from dataclasses import asdict

    settings = Settings()
    settings_dict = asdict(settings)
    print(settings_dict)
    ```

    Output:

    ```python
    {'debug': True, 'port': 8080, 'ruleset_path': PosixPath('ruleset.yaml')}
    ```

1. Also you can redefine some values in runtime and create new instance of Settings:

    ```python
    settings = Settings(port=80)
    settings_dict = asdict(settings)
    print(settings_dict)
    ```

    Output:

    ```python
    {'debug': True, 'port': 80, 'ruleset_path': PosixPath('ruleset.yaml')}
    ```

## Features:

- [x] env vars
- [x] configuration via values in dotenv file
  Should install dataclasses-settings with extra-package `pip install "git+https://github.com/shpaker/dataclasses-settings.git#egg=project [dotenv]"`
