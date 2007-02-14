##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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
"""Setup for zope.traversing package

$Id$
"""

import os

from setuptools import setup, find_packages

setup(name='zope.traversing',
      version='3.4dev',
      url='http://svn.zope.org/zope.traversing',
      license='ZPL 2.1',
      description='Zope traversing',
      author='Zope Corporation and Contributors',
      author_email='zope3-dev@zope.org',
      long_description="Module for traversing the object tree.",

      packages=find_packages('src'),
	  package_dir = {'': 'src'},

      namespace_packages=['zope',],
      tests_require = ['zope.testing',
                       'zope.annotation',
                       'zope.location',
                       ],
      install_requires=['zope.interface',
                        'zope.proxy',
                        'zope.component',
                        'zope.i18n',
                        'zope.i18nmessageid',
                        'zope.publisher',
                        'zope.security',
                        ],
      include_package_data = True,

      zip_safe = False,
      )
