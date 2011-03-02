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
      version='3.14.0',
      url='http://pypi.python.org/pypi/zope.traversing',
      license='ZPL 2.1',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      description="Resolving paths in the object hierarchy",
      long_description=long_description,

      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope',],
      extras_require = dict(test=['zope.browserpage',
                                  'zope.browserresource[zcml]>=3.12',
                                  'zope.component[zcml]',
                                  'zope.configuration',
                                  'zope.container',
                                  'zope.pagetemplate',
                                  'zope.security[zcml]>=3.8',
                                  'zope.site',
                                  'zope.tal >= 3.5.0',
                                  'zope.testing',
                                  'ZODB3',
                                  ]),
      install_requires=['setuptools',
                        'zope.component',
                        'zope.i18n',
                        'zope.i18nmessageid',
                        'zope.interface',
                        'zope.proxy',
                        'zope.publisher',
                        'zope.security',
                        'zope.location>=3.7.0',
                        ],
      include_package_data = True,
      zip_safe = False,
      )
