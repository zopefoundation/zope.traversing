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
"""
$Id: test_physicallocationadapters.py,v 1.15 2003/11/21 17:12:16 jim Exp $
"""

from unittest import TestCase, main, makeSuite
from zope.app.tests.placelesssetup import PlacelessSetup
from zope.app.tests import ztapi
from zope.component import getAdapter
from zope.interface import implements

from zope.app.interfaces.traversing import IContainmentRoot
from zope.app.interfaces.traversing import IPhysicallyLocatable
from zope.app.location import LocationPhysicallyLocatable
from zope.app.traversing.adapters import RootPhysicallyLocatable
from zope.app.container.contained import contained

class Root:
    implements(IContainmentRoot)

class C:
    pass

class Test(PlacelessSetup, TestCase):

    def test(self):
        ztapi.provideAdapter(None, IPhysicallyLocatable,
                             LocationPhysicallyLocatable)
        ztapi.provideAdapter(IContainmentRoot, IPhysicallyLocatable,
                             RootPhysicallyLocatable)

        root = Root()
        f1 = contained(C(), root, name='f1')
        f2 = contained(C(),   f1, name='f2')
        f3 = contained(C(),   f2, name='f3')

        adapter = getAdapter(f3, IPhysicallyLocatable)

        self.assertEqual(adapter.getPath(), '/f1/f2/f3')
        self.assertEqual(adapter.getName(), 'f3')
        self.assertEqual(adapter.getRoot(), root)


def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')
