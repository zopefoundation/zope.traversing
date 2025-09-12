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

from setuptools import setup


def read(filename):
    with open(filename) as f:
        return f.read()


long_description = (read('README.rst') +
                    '\n\n' +
                    read('CHANGES.rst'))


TESTS_REQUIRE = [
    'zope.annotation',
    'zope.browserresource[zcml]>=3.12',
    'zope.component[zcml]',
    'zope.configuration',
    'zope.security[zcml]>=3.8',
    'zope.tales',
    'zope.testing',
    'zope.testrunner >= 6.4'
]

setup(
    name='zope.traversing',
    version='6.0',
    url='https://github.com/zopefoundation/zope.traversing',
    license='ZPL-2.1',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.dev',
    description="Resolving paths in the object hierarchy",
    long_description=long_description,
    keywords="zope traversal route URL view",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
        'docs': [
            'Sphinx',
            'repoze.sphinx.autointerface',
        ],
    },
    install_requires=[
        'setuptools',
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
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.9',
)
