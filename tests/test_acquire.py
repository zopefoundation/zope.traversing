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
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""

Revision information:
$Id: test_acquire.py,v 1.8 2003/09/21 17:31:14 jim Exp $
"""

from unittest import TestCase, main, makeSuite
from zope.app.tests.placelesssetup import PlacelessSetup
from zope.app.interfaces.traversing import ITraversable
from zope.app.traversing.adapters import DefaultTraversable
from zope.component.adapter import provideAdapter
from zope.app.traversing.namespace import acquire
from zope.exceptions import NotFoundError

class Test(PlacelessSetup, TestCase):

    def test(self):
        provideAdapter(None, ITraversable, DefaultTraversable)

        class C:
            def __init__(self, name):
                self.name = name

        a = C('a')
        a.a1 = C('a1')
        a.a2 = C('a2'); a.a2.__parent__ = a
        a.a2.a21 = C('a21'); a.a2.a21.__parent__ = a.a2
        a.a2.a21.a211 = C('a211'); a.a2.a21.a211.__parent__ = a.a2.a21

        a2 = a.a2
        a21 = a.a2.a21
        a211 = a.a2.a21.a211

        acquired = acquire('a1', (), 'a1;acquire', a211, None)

        self.assertEqual(acquired.name, 'a1')

        self.assertRaises(NotFoundError,
                          acquire, 'a3', (), 'a1;acquire', a211, None)



def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')
