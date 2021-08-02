import json
from dataclasses import field, is_dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from dataclasses_settings.decorator import dataclass_settings
from dataclasses_settings.env import read_env_vars
from dataclasses_settings.params import field_params


def test_read_env_vars():
    env_vars = read_env_vars(
        prefix="test_",
    )
    assert env_vars


def test_decorator(
    test_env_vars: Dict[str, str],
) -> None:
    @dataclass_settings
    class Settings:
        test_env_key: str

    settings = Settings()
    assert settings.test_env_key == test_env_vars["test_env_key"]


def test_decorator_with_field(
    test_env_vars: Dict[str, str],
) -> None:
    @dataclass_settings
    class Settings:
        test_env_key: str = field(default="test")

    settings = Settings()
    assert settings.test_env_key == test_env_vars["test_env_key"]


def test_decorator_with_alias(
    test_env_vars: Dict[str, str],
) -> None:
    @dataclass_settings(prefix="test_")
    class Settings:
        some_field: str = field(default="test", metadata=field_params(alias="env_key"))

    settings = Settings()
    assert settings.some_field == test_env_vars["test_env_key"]


def test_none() -> None:
    @dataclass_settings(prefix="test_")
    class Settings:
        none: None

    settings = Settings()
    assert settings.none is None


def test_optional(
    test_env_vars: Dict[str, str],
) -> None:
    @dataclass_settings
    class Settings:
        test_env_key: Optional[str]

    settings = Settings()
    assert settings.test_env_key == test_env_vars["test_env_key"]

    @dataclass_settings
    class Settings:  # pylint: disable=function-redefined
        test_none: Optional[int]

    settings = Settings()
    assert settings.test_none is None


def test_empty_optional() -> None:
    try:

        @dataclass_settings
        class Settings:
            test_env_key: Optional

        Settings()
        assert False
    except ValueError:
        pass


def test_decorator_with_str(
    test_env_vars: Dict[str, str],
) -> None:
    @dataclass_settings(prefix="test_")
    class Settings:
        env_int: str

    settings = Settings()
    assert isinstance(settings.env_int, str)
    assert settings.env_int == test_env_vars["test_env_int"]


def test_decorator_with_bool(
    test_env_vars: Dict[str, str],  # pylint: disable=unused-argument
) -> None:
    @dataclass_settings(prefix="test_")
    class Settings:
        env_bool: bool

    settings = Settings()
    assert isinstance(settings.env_bool, bool)
    assert settings.env_bool is True


def test_decorator_with_int(
    test_env_vars: Dict[str, str],
) -> None:
    @dataclass_settings(prefix="test_")
    class Settings:
        env_int: int

    settings = Settings()
    assert isinstance(settings.env_int, int)
    assert settings.env_int == int(test_env_vars["test_env_int"])


def test_decorator_with_float(
    test_env_vars: Dict[str, str],
) -> None:
    @dataclass_settings(prefix="test_")
    class Settings:
        env_int: float

    settings = Settings()
    assert isinstance(settings.env_int, float)
    assert settings.env_int == float(test_env_vars["test_env_int"])


def test_decorator_with_list(
    test_env_vars: Dict[str, str],
) -> None:
    @dataclass_settings(prefix="test_")
    class Settings:
        env_list: list

    settings = Settings()
    assert settings.env_list == json.loads(test_env_vars["test_env_list"])


def test_decorator_with_datetime(
    test_env_vars: Dict[str, str],
) -> None:
    @dataclass_settings(prefix="test_")
    class Settings:
        env_datetime: datetime

    settings = Settings()
    assert settings.env_datetime == datetime.fromisoformat(test_env_vars["test_env_datetime"])


def test_decorator_with_timedelta(
    test_env_vars: Dict[str, str],
) -> None:
    @dataclass_settings(prefix="test_")
    class Settings:
        env_timedelta: timedelta

    settings = Settings()
    assert settings.env_timedelta == timedelta(seconds=int(test_env_vars["test_env_timedelta"]))


def test_decorator_with_str_enum(
    test_env_vars: Dict[str, str],
) -> None:
    class TestStrEnum(str, Enum):
        TEST = test_env_vars["test_env_str_enum"]

    @dataclass_settings(prefix="test_")
    class Settings:
        env_str_enum: TestStrEnum

    settings = Settings()
    assert settings.env_str_enum is TestStrEnum.TEST


def test_decorator_with_int_enum(
    test_env_vars: Dict[str, str],
) -> None:
    class TestIntEnum(str, Enum):
        TEST = int(test_env_vars["test_env_int_enum"])

    @dataclass_settings(prefix="test_")
    class Settings:
        env_int_enum: TestIntEnum

    settings = Settings()
    assert settings.env_int_enum is TestIntEnum.TEST


def test_decorator_with_dict(
    test_env_vars: Dict[str, str],
) -> None:
    @dataclass_settings(prefix="test_")
    class Settings:
        env_dict: dict

    settings = Settings()
    assert settings.env_dict == json.loads(test_env_vars["test_env_dict"])


def test_decorator_with_union(
    test_env_vars: Dict[str, str],  # pylint: disable=unused-argument
) -> None:
    @dataclass_settings(prefix="test_")
    class Settings:
        env_dict: Union[int, float, Dict[str, Any], List[str]]

    settings = Settings()
    assert settings.env_dict == json.loads(test_env_vars["test_env_dict"])


def test_decorator_with_path(
    test_env_vars: Dict[str, str],  # pylint: disable=unused-argument
) -> None:
    @dataclass_settings(prefix="test_")
    class Settings:
        env_int: Path

    settings = Settings()
    assert isinstance(settings.env_int, Path)


def test_decorator_with_unknown_type(
    test_env_vars: Dict[str, str],  # pylint: disable=unused-argument
) -> None:

    try:

        @dataclass_settings(prefix="test_")
        class Settings:
            env_int: UUID

        settings = Settings()
        assert False, settings.env_int
    except ValueError:
        pass


def test_decorator_with_prefix(
    test_env_vars: Dict[str, str],
) -> None:
    @dataclass_settings(prefix="test_")
    class Settings:
        env_key: str

    settings = Settings()
    assert settings.env_key == test_env_vars["test_env_key"]


def test_decorator_dataclass(
    test_env_vars: Dict[str, str],
) -> None:
    @dataclass_settings(prefix="test_", frozen=True)
    class Settings:
        env_key: str

    settings = Settings()
    assert is_dataclass(settings)
    assert settings.env_key == test_env_vars["test_env_key"]
