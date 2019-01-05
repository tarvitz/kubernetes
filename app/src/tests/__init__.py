import os
import json

from unittest import mock

from backend.consts import HttpStatus

_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RESOURCE_DIR = os.path.join(_BASE_DIR, 'resources/tests')


class MockEnv(object):
    """
    Helps to override os.environment with your settings
    usage:

    .. code-block:: python

        with MockEnv({'ENV': 'Me'}):
            assert os.environ.get('ENV') == 'Me'
    """

    def __init__(self, override):
        """
        :param dict override: override os.environment
        """
        self.override = override
        self._event = None

    def __enter__(self):
        self._event = mock.patch.dict(os.environ, self.override)
        self._event.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._event.stop()
        return


class ResourceMixin(object):
    @staticmethod
    def get_resource_path(rel_path):
        """
        Gets resource according to resources dir bound in package

        :param str rel_path: related path started from resource dir
        :rtype: str
        :return: path to resource
        """
        return os.path.join(RESOURCE_DIR, rel_path)

    @staticmethod
    def get_resource(rel_path, mode='rb'):
        """
        Gets resource file object according to resources dir bound in package

        :param str rel_path: related path started from resource dir
        :param str mode: file open mode
        :rtype: io.TextIOWrapper
        :return: path to resource
        """
        return open(ResourceMixin.get_resource_path(rel_path), mode)


class FakeResponse(object):
    """
    Very tiny :py:class:`requests.Response` mock class
    """
    def __init__(self, content,
                 content_type='application/json',
                 status=HttpStatus.OK):
        self.status_code = status
        self.content_type = content_type
        self.content = content

    def json(self):
        return json.loads(self.content)
