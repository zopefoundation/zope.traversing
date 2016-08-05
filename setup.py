##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.traversing package
"""
import os
import sys
from setuptools import setup, find_packages


def read(filename):
    with open(filename) as f:
        return f.read()

long_description = (read('README.rst') +
                    '\n\n' +
                    read('CHANGES.rst'))


def test_suite():
    # use the zope.testrunner machinery to find all the
    # test suites we've put under ourselves
    from zope.testrunner.options import get_options
    from zope.testrunner.find import find_suites
    from unittest import TestSuite
    here = os.path.abspath(os.path.dirname(sys.argv[0]))
    args = sys.argv[:]
    src = os.path.join(here, 'src')
    defaults = ['--test-path', src]
    options = get_options(args, defaults)
    suites = list(find_suites(options))
    return TestSuite(suites)

TESTS_REQUIRE = [
    'zope.annotation',
    'zope.browserresource[zcml]>=3.12',
    'zope.component[zcml]',
    'zope.configuration',
    'zope.security[zcml]>=3.8',
    'zope.tales',
    'zope.testing',
    'zope.testrunner'
]

setup(
    name='zope.traversing',
    version='4.1.0',
    url='http://pypi.python.org/pypi/zope.traversing',
    license='ZPL 2.1',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    description="Resolving paths in the object hierarchy",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['zope'],
    extras_require=dict(test=TESTS_REQUIRE),
    install_requires=[
        'setuptools',
        'six',
        'transaction',
        'zope.component',
        'zope.i18n',
        'zope.i18nmessageid',
        'zope.interface>=4.0.4',
        'zope.location>=3.7.0',
        'zope.proxy',
        'zope.publisher',
        'zope.security',
    ],
    tests_require=TESTS_REQUIRE,
    test_suite='__main__.test_suite',
    include_package_data=True,
    zip_safe=False,
)
