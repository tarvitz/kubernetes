import unittest
import argparse

from backend.server.argparse import Environment

from ... import MockEnv


class EnvironmentCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = argparse.ArgumentParser()
        cls.parser = parser

    def test_env_and_non_default(self):
        with MockEnv({
            'LOCAL_URL': 'https://localhost:8000/',
        }):
            self.parser.add_argument(
                '-u', '--url', dest='url',
                action=Environment, env_name="LOCAL_URL",
                required=True
            )
            #: fallback to api instead of using sys.args
            args = self.parser.parse_args([])
            self.assertEqual(args.url, 'https://localhost:8000/')
            #: test priority
            args = self.parser.parse_args(['-u', 'https://example.org'])
            self.assertEqual(args.url, 'https://example.org')
            self.assertNotEqual(args.url, 'https://localhost:8000/')

    def test_env_and_default(self):
        with MockEnv({
            'LOCAL_URL': 'https://example.org',  # bypassing required
            'PORT': '9000'
        }):
            self.parser.add_argument(
                '-p', '--port', dest='port', default=8000, type=int,
                action=Environment, env_name='PORT',
                required=False
            )
            #: fallback to api instead of using sys.args
            args = self.parser.parse_args([])
            self.assertEqual(args.port, 9000)

            #: test priority
            args = self.parser.parse_args(['-p', '8888'])
            self.assertEqual(args.port, 8888)
