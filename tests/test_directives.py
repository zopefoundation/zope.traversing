##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Test the traversalNamespace directive.

$Id: test_directives.py,v 1.1 2003/08/02 18:17:28 srichter Exp $
"""
import unittest

from zope.app.traversing.namespace import _namespace_handlers 
from zope.configuration import xmlconfig
import zope.app.traversing.tests

class Handler:
    pass
  
class DirectivesTest(unittest.TestCase):

    def test_traversalNamespace(self):
        self.assertEqual(_namespace_handlers.get('test', None), None)
        self.context = xmlconfig.file("traversing.zcml",
                                      zope.app.traversing.tests)
        self.assertEqual(_namespace_handlers.get('test'), Handler)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(DirectivesTest),
        ))

if __name__ == '__main__':
    unittest.main()
