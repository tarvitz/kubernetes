"""
Very straight forward and simple utils
To boost settings work. In case if you would like
"""

import os
import ast
import pkg_resources

PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(__file__))


def _get_literal_from_env(env_key, fallback):
    """
    reads environment variable and tries to covert it to python literal

    :param str env_key:
    :param object fallback: fallback value
    :rtype: object
    :return: python literal
    """
    try:
        value = ast.literal_eval(os.environ.get(env_key))
        return value
    except ValueError:
        return fallback


def get_env_bool(env_key, fallback):
    """
    reads boolean literal from environment.

    Please note that 0, [], {}, '' treats as False

    :param str env_key: key to read
    :param bool fallback: fallback value
    :rtype: bool
    :return: environment value typed in bool
    """
    assert isinstance(fallback, bool), "fallback should be bool instance"
    return bool(_get_literal_from_env(env_key, fallback))


def get_env_int(env_key, fallback):
    """
    reads boolean literal from environment.

    Please note that 0, [], {}, '' treats as False

    :param str env_key: key to read
    :param int fallback: fallback value
    :rtype: int
    :return: environment value typed in bool
    """
    assert isinstance(fallback, int), "fallback should be int instance"
    return _get_literal_from_env(env_key, fallback)


def get_env_string(env_key, fallback):
    """
    reads boolean literal from environment. (does not use literal compilation
    as far as env returns always a string value

    Please note that 0, [], {}, '' treats as False

    :param str env_key: key to read
    :param str fallback: fallback value
    :rtype: str
    :return: environment value typed in string
    """
    assert isinstance(fallback, str), "fallback should be str instance"
    return os.environ.get(env_key) or fallback


def rel(path, base_dir=PROJECT_ROOT_DIR):
    return os.path.join(base_dir, path)


def requires(dependencies, *, validator=all):
    """
    Checks if package has dependencies according to `validator` logic

    :param list[str] | tuple[str] dependencies: list of dependencies without
        its versions, for example: raven, requests, wheel, setuptools, etc
    :param callable validator: boolean sequence validator, by default
        it's :py:func:`all`. Recommended to use:

        - :py:func:`all`
        - :py:func:`any`
    :return: decorator
    """

    #: a bit hacky, however setuptools is a root dependency anyway
    distribution = pkg_resources.get_distribution('setuptools')
    has_resource = distribution.has_resource

    def decorator(func):
        def wrapper(*args, **kwargs):
            have_all_dependencies = validator(map(has_resource, dependencies))
            if have_all_dependencies:
                return func(*args, **kwargs)
            return
        return wrapper
    return decorator
