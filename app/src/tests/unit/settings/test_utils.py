import unittest

from backend.settings import utils

from ... import MockEnv


class UtilsTestCase(unittest.TestCase):
    """
    Utils Common Test Case
    """

    def test_get_literal_eval(self):
        self.assertEqual(
            utils._get_literal_from_env("NON_EXISTENT", 'fallback'), 'fallback'
        )
        with MockEnv({
            'DICT': '{"a": 1}',
            'PYTHON_TYPE_ERROR': 'string',
            'PYTHON_STRING': '"string"',
            'PYTHON_INT': '5432'
        }):
            self.assertEqual(utils._get_literal_from_env('DICT', {}), {'a': 1})
            self.assertEqual(utils._get_literal_from_env(
                'PYTHON_TYPE_ERROR', 'fallback'), 'fallback'
            )
            self.assertEqual(utils._get_literal_from_env(
                'PYTHON_STRING', 'fallback'), 'string'
            )
            self.assertEqual(utils._get_literal_from_env('PYTHON_INT', 0),
                             5432)

    def test_get_env_fallback_assertion(self):
        with self.assertRaises(AssertionError):
            utils.get_env_bool("ENV", 'string')

        with self.assertRaises(AssertionError):
            utils.get_env_string("ENV", 1)

    def test_get_env_common(self):
        """
        tests get_env_string, get_env_bool, etc legit output
        """
        self.assertFalse(utils.get_env_bool('ENV', fallback=False))
        self.assertEqual(utils.get_env_string('ENV', fallback="fallback"),
                         "fallback")
        self.assertEqual(utils.get_env_int('ENV', fallback=1), 1)

    def test_rel(self):
        self.assertNotEqual(utils.rel('static'), '/static/')

    @staticmethod
    def foo():
        return 'bar'

    def test_requires(self):
        #: ok
        self.assertEqual(utils.requires(['setuptools'])(self.foo)(), 'bar')
        #: ok with partial dependency list
        self.assertEqual(
            utils.requires(['setuptools', 'non-existent-deps'],
                           validator=any)(self.foo)(), 'bar'
        )

        #: skip due to insufficient dependency
        self.assertEqual(
            utils.requires(['non-existent-deps'])(self.foo)(),
            None
        )
