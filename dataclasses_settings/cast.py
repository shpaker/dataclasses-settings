from datetime import datetime, timedelta
from enum import Enum, IntEnum
from json import loads
from pathlib import Path
from typing import Any, Union

BOOL_TRUE_VALUES = ("+", "y", "yes", "true", "on")
BOOL_FALSE_VALUES = ("-", "n", "no", "false", "off")
NONE_VALUE = ("none", "null", "~", "")


# pylint: disable=too-many-return-statements,too-many-branches
def _cast_value(
    value: str,
    cast_type: type,
) -> Any:

    if cast_type is str:
        return value
    if cast_type in (int, float, Path):
        return cast_type(value)

    if cast_type is None or cast_type is type(None):  # noqa
        if value.lower().strip() in NONE_VALUE:
            return None

    if cast_type is bool:
        if value.lower().strip() in BOOL_TRUE_VALUES:
            return True
        if value.lower().strip() in BOOL_FALSE_VALUES:
            return False
        raise ValueError

    try:
        origin = cast_type.__origin__
    except AttributeError:
        origin = None

    if origin is Union:
        args = cast_type.__args__
        for arg in args:
            try:
                return _cast_value(value, arg)
            except ValueError:
                ...
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

    raise ValueError(f"Type not yet supported: {cast_type}")
