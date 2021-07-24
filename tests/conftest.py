from os import environ
from typing import Dict

from pytest import fixture


@fixture(
    name="test_env_vars",
    scope="session",
)
def testing_env_vars_fixture() -> Dict[str, str]:
    return {
        "test_env_key": "env_value",
        "test_env_int": "1234567890",
        "test_env_list": '[1, 2, "4"]',
        "test_env_dict": '{"foo": "bar"}',
        "test_env_datetime": "2005-08-09T18:31:42",
        "test_env_timedelta": "120",
        "test_env_int_enum": "999",
        "test_env_str_enum": "str_enum_value",
        "test_env_bool": "yes",
    }


@fixture(
    autouse=True,
    scope="session",
)
def set_env_vars_fixture(
    test_env_vars: Dict[str, str],
):
    environ.update(test_env_vars)
