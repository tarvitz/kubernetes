#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test

#: consider using setuptools_scm instead of declaring static version
version = "1.0"


class DjangoTest(test):
    user_options = [("django-test-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        test.initialize_options(self)
        self.django_test_args = ""

    def run_tests(self):
        import django
        from django.conf import settings
        from django.test.utils import get_runner

        os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
        django.setup()

        test_runner_class = get_runner(settings)
        #: django.test.runner.DiscoverRunner, additional options does not
        #: work for now
        test_runner = test_runner_class()
        failures = test_runner.run_tests(["tests"])
        sys.exit(bool(failures))


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Indented Audience :: System Administrators',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Natural Language :: English',
    'Topic :: Utilities',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.6'
]

install_requires = [
    #: BSD licenses
    'Django==2.2.28',
]
test_requires = []


setup(
    name='backend',
    author='Nickolas Fox <tarvitz@blacklibrary.ru>',
    version=version,
    author_email='tarvitz@blacklibrary.ru',
    description='Backend Application',
    long_description="",
    license='BSD',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=install_requires,
    test_requires=test_requires,
    packages=find_packages(
        exclude=('tests', 'resources')
    ),
    entry_points={
        'console_scripts': [
            'site-manage = backend.manage:main',
            'wsgi-server = backend.server.__main__:main'
        ]
    },
    package_data={
        '': ['templates/*', 'conf/*']
    },
    include_package_data=True,
    test_suite='tests',
    zip_safe=False,
    cmdclass={"django_test": DjangoTest}
)
