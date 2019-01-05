import os
import argparse


def void(argument):
    return argument


class Environment(argparse.Action):
    @staticmethod
    def _get_default_overrode(default, env_name, _type=void):
        """
        Get overrode default value from environment variable and applying
        type for it or bypassing

        :param object default: setup default value
        :param str env_name: environment variable
        :param callable _type: type to convert value taken from environment
            if applicable
        :rtype: object
        :return: value of passed `_type` or str
        """
        value = os.environ.get(env_name) or None
        if value is None:
            return default
        return _type(value)

    def __init__(self, env_name, required=True, default=None, **kwargs):
        default = self._get_default_overrode(
            default, env_name, _type=kwargs.get('type', void))

        if required and default:
            required = False

        super().__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
