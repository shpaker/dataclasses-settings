# dataclass-settings

Oversimplified decorator for settings management (via environment variables) with built in dataclasses superpowers.

## Installation

Install using `pip install dataclass-settings -U`.

## Usage

1. Specify environments variables:

    ```shell
    export APP_PORT=8080
    export APP_DEBUG=yes
    export APP_RULESET_PATH=./ruleset.yaml
    ```

1. Define class for settings of your app:

    ```python
    from pathlib import Path
    from typing import Optional

    from dataclass_settings import dataclass_settings


    @dataclass_settings(prefix="app_", frozen=True)
    class Settings:
        host: str = "0.0.0.0"
        port: int
        debug: bool = True
        ruleset_path: Optional[Path] = None
    ```

1. Use this with lru_cache

    ```python
    from functools import lru_cache

    @lru_cache()
    def get_setting():
        return Settings()
    ```
