from dataclasses import Field, dataclass, field
from pathlib import Path
from typing import Any, MutableMapping, MutableSequence, MutableSet

from dataclasses_settings.cast import _cast_value
from dataclasses_settings.env import read_env_vars

MUTABLE_TYPES = (
    MutableSequence,
    MutableSet,
    MutableMapping,
)


def _check_value(
    value: Any,
    cls: object,
    attr_key: str,
) -> Any:
    is_mutable = issubclass(type(value), MUTABLE_TYPES)
    try:
        attr_value = getattr(cls, attr_key)
        if is_mutable:
            if isinstance(attr_value, Field):
                attr_value.default_factory = lambda: value
                return attr_value
            return field(default_factory=lambda: value)
        attr_value.default = value if isinstance(attr_value, Field) else value
        return attr_value
    except AttributeError:
        return field(default_factory=lambda: value) if is_mutable else field(default=value)


def dataclass_settings(
    cls=None,
    prefix: str = "",
    case_sensitive: bool = False,
    dotenv_path: Path = None,
    dotenv_encoding: str = None,
    **kwargs,
):
    def wrap(arg):
        env_vars = read_env_vars(
            prefix=prefix,
            case_sensitive=case_sensitive,
            dotenv_path=dotenv_path,
            dotenv_encoding=dotenv_encoding,
        )
        for attr_key, attr_type in arg.__annotations__.items():
            if attr_key in env_vars:
                value = _cast_value(
                    attr_key,
                    env_vars[attr_key],
                    attr_type,
                )
                attr_value = _check_value(
                    value=value,
                    cls=arg,
                    attr_key=attr_key,
                )
                setattr(arg, attr_key, attr_value)
        return dataclass(arg, **kwargs)

    if cls is None:
        return wrap
    return wrap(cls)
