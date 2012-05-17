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
from setuptools import setup, find_packages

long_description = (open('README.txt').read() +
                    '\n\n' +
                    open('CHANGES.txt').read())

setup(name='zope.traversing',
      version='4.0.0dev',
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        ],
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope',],
      extras_require = dict(test=[
          'ZODB3',
          'zope.annotation',
          'zope.browserresource[zcml]>=3.12',
          'zope.component[zcml]',
          'zope.configuration',
          'zope.container',
          'zope.pagetemplate',
          'zope.security[zcml]>=3.8',
          'zope.site',
          'zope.testing',
          ]),
      install_requires=[
          'setuptools',
          'zope.browserpage',
          'zope.component',
          'zope.i18n',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.location>=3.7.0',
          'zope.proxy',
          'zope.publisher',
          'zope.security',
          ],
      include_package_data = True,
      zip_safe = False,
      )
