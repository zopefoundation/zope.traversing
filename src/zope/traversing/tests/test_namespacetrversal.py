##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""Traversal Namespace Tests
"""
import re
from unittest import main
from doctest import DocTestSuite
from zope.component.testing import setUp, tearDown
from zope.testing.renormalizing import RENormalizing



def test_suite():
    checker = RENormalizing([
        # Python 3 includes module name in exceptions
        (re.compile(r"zope.location.interfaces.LocationError"),
         "LocationError"),
    ])

    return DocTestSuite('zope.traversing.namespace',
                        setUp=setUp, tearDown=tearDown,
                        checker=checker)

if __name__ == '__main__':
    main(defaultTest='test_suite')
