from datetime import datetime, timedelta
from enum import Enum, IntEnum
from json import loads
from pathlib import Path
from typing import Any, Union, get_origin

BOOL_TRUE_VALUES = ("+", "y", "yes", "true", "on")
BOOL_FALSE_VALUES = ("-", "n", "no", "false", "off")


def _cast_value(
    key: str,
    value: str,
    cast_type: type,
) -> Any:

    if cast_type is str:
        return value
    if cast_type in (int, float, Path):
        return cast_type(value)

    if cast_type is bool:
        if value.lower() in BOOL_TRUE_VALUES:
            return True
        if value.lower() in BOOL_FALSE_VALUES:
            return False
        raise ValueError(f"{key}: incorrect boolean value: {value}")

    origin = get_origin(cast_type)

    if origin is Union:
        raise ValueError(f"{key}: currently doesn't support Union types")
    if origin:
        cast_type = origin

    if issubclass(cast_type, Enum) and issubclass(cast_type, str):
        return cast_type(value)
    if issubclass(cast_type, IntEnum) or (issubclass(cast_type, Enum) and issubclass(cast_type, int)):
        return cast_type(int(value))

    if cast_type is dict:
        return loads(value)
    if cast_type in (list, set, tuple):
        result = loads(value)
        if isinstance(result, list):
            return result
        return cast_type(result)

    if cast_type is datetime:
        return datetime.fromisoformat(value)
    if cast_type is timedelta:
        return timedelta(seconds=int(value))

    raise ValueError(f"{key}: type not yet supported: {cast_type}")
