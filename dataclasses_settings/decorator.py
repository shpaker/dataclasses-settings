from dataclasses import dataclass
from pathlib import Path

from dataclasses_settings.cast import _cast_value
from dataclasses_settings.env import read_env_vars


def env_settings(
    cls=None,
    prefix: str = "",
    case_sensitive: bool = False,
    dotenv_path: Path = None,
    dotenv_encoding: str = None,
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
                setattr(arg, attr_key, value)
        return arg

    if cls is None:
        return wrap
    return wrap(cls)


def dataclass_settings(
    cls=None,
    prefix: str = "",
    case_sensitive: bool = False,
    dotenv_path: Path = None,
    dotenv_encoding: str = None,
    **kwargs,
):
    def wrap(arg):
        return dataclass(
            env_settings(
                cls=arg,
                prefix=prefix,
                case_sensitive=case_sensitive,
                dotenv_path=dotenv_path,
                dotenv_encoding=dotenv_encoding,
            ),
            **kwargs,
        )

    if cls is None:
        return wrap

    return wrap(cls)
