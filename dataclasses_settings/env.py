from os import environ
from pathlib import Path
from typing import Dict, Mapping


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
        env_vars = dict((k.lower(), v) for k, v in env_vars.items())
    if prefix:
        env_vars = dict((_check_prefix(k, prefix), v) for k, v in env_vars.items() if k.startswith(prefix))
    return env_vars


def read_vars(
    dotenv_path: Path = None,
    encoding: str = None,
) -> Dict[str, str]:
    if dotenv_path:
        encoding = encoding or "utf8"
        return read_dotenv_vars(dotenv_path, encoding)
    return dict(environ)


def read_env_vars(
    prefix: str = None,
    case_sensitive: bool = False,
    dotenv_path: Path = None,
    dotenv_encoding: str = None,
) -> Mapping[str, str]:
    env_vars = read_vars(dotenv_path, dotenv_encoding)
    return _check_env_vars(env_vars, prefix, case_sensitive)


def read_dotenv_vars(
    dotenv_path: Path,
    dotenv_encoding: str,
) -> Dict[str, str]:
    try:
        from dotenv import dotenv_values  # pylint: disable=import-outside-toplevel
    except ImportError as err:
        raise ImportError("Should install 'python-dotenv' package") from err
    return dotenv_values(dotenv_path, encoding=dotenv_encoding)
