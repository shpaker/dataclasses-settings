from dataclasses import Field, dataclass, field
from pathlib import Path
from typing import Any, List, MutableMapping, MutableSequence, MutableSet, Tuple

from dataclasses_settings.cast import _cast_value
from dataclasses_settings.env import read_env_vars
from dataclasses_settings.exceptions import ValidationError

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
    except AttributeError:
        if is_mutable:
            return field(default_factory=lambda: value)
        return field(default=value)
    if is_mutable:
        if isinstance(attr_value, Field):
            attr_value.default_factory = lambda: value
            return attr_value
        return field(default_factory=lambda: value)
    attr_value.default = value if isinstance(attr_value, Field) else value
    return attr_value


def dataclass_settings(
    cls=None,
    prefix: str = "",
    case_sensitive: bool = False,
    dotenv_path: Path = None,
    dotenv_encoding: str = None,
    **kwargs,
):
    if "frozen" not in kwargs:
        kwargs["frozen"] = True

    def wrap(arg):
        env_vars = read_env_vars(
            prefix=prefix,
            case_sensitive=case_sensitive,
            dotenv_path=dotenv_path,
            dotenv_encoding=dotenv_encoding,
        )
        errors: List[Tuple[str, str, str]] = list()
        for attr_key, attr_type in arg.__annotations__.items():
            key_alias = None
            try:
                attr_value = getattr(arg, attr_key)
                if isinstance(attr_value, Field):
                    key_alias = attr_value.metadata.get("alias")
            except AttributeError:
                pass

            if (key_alias or attr_key) in env_vars:
                try:
                    value = _cast_value(
                        env_vars[key_alias or attr_key],
                        attr_type,
                    )
                except (TypeError, ValueError):
                    errors.append((attr_key, env_vars[attr_key], "incorrect or unknown type"))
                    continue
                attr_value = _check_value(
                    value=value,
                    cls=arg,
                    attr_key=attr_key,
                )
                setattr(arg, attr_key, attr_value)
        if errors:
            raise ValidationError(errors)
        return dataclass(arg, **kwargs)

    if cls is None:
        return wrap
    return wrap(cls)
