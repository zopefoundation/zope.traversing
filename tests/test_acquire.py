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
$Id: test_acquire.py,v 1.4 2002/12/28 17:49:34 stevea Exp $
"""

from unittest import TestCase, TestSuite, main, makeSuite
from zope.app.tests.placelesssetup import PlacelessSetup
from zope.app.interfaces.traversing import ITraversable
from zope.app.traversing.adapters import DefaultTraversable
from zope.component.adapter import provideAdapter
from zope.proxy.context import ContextWrapper, getWrapperContext
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
        a.a2 = C('a2')
        a.a2.a21 = C('a21')
        a.a2.a21.a211 = C('a211')

        a2 = ContextWrapper(a.a2, a)
        a21 = ContextWrapper(a.a2.a21, a2)
        a211 = ContextWrapper(a.a2.a21.a211, a21)

        acquired = acquire('a1', (), 'a1;acquire', a211, None)

        self.assertEqual(acquired.name, 'a1')

        self.assertRaises(NotFoundError,
                          acquire, 'a3', (), 'a1;acquire', a211, None)



def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')
