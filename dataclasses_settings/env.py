from os import environ
from typing import Mapping


def _check_prefix(
    string: str,
    prefix: str,
) -> str:
    return string[len(prefix) :] if string.startswith(prefix) else string  # noqa


def _check_env_vars(
    env_vars: Mapping[str, str],
    prefix: str,
    case_sensitive: bool,
) -> Mapping[str, str]:
    if not case_sensitive:
        prefix = prefix.lower()
        env_vars = {k.lower(): v for k, v in env_vars.items()}
    if prefix:
        env_vars = {_check_prefix(k, prefix): v for k, v in env_vars.items() if k.startswith(prefix)}
    return env_vars


def read_env_vars(
    prefix: str = "",
    case_sensitive: bool = False,
) -> Mapping[str, str]:
    env_vars: Mapping[str, str] = dict(environ)
    return _check_env_vars(env_vars, prefix, case_sensitive)
