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
$Id: test_physicallocationadapters.py,v 1.7 2003/05/01 19:35:38 faassen Exp $
"""

from unittest import TestCase, main, makeSuite
from zope.app.tests.placelesssetup import PlacelessSetup
from zope.component.adapter import provideAdapter
from zope.component import getAdapter

from zope.app.interfaces.traversing import IContainmentRoot
from zope.app.interfaces.traversing import IPhysicallyLocatable
from zope.app.traversing.adapters import WrapperPhysicallyLocatable
from zope.app.traversing.adapters import RootPhysicallyLocatable
from zope.proxy.context import ContextWrapper

class Root: __implements__ = IContainmentRoot
class C: pass

class Test(PlacelessSetup, TestCase):

    def test(self):
        provideAdapter(None, IPhysicallyLocatable, WrapperPhysicallyLocatable)
        provideAdapter(IContainmentRoot, IPhysicallyLocatable,
                       RootPhysicallyLocatable)

        root = Root()
        f1 = ContextWrapper(C(), root, name='f1')
        f2 = ContextWrapper(C(),   f1, name='f2')
        f3 = ContextWrapper(C(),   f2, name='f3')

        adapter = getAdapter(f3, IPhysicallyLocatable)

        self.assertEqual(adapter.getPath(), '/f1/f2/f3')
        self.assertEqual(adapter.getRoot(), root)

        adapter = getAdapter(C(), IPhysicallyLocatable)
        self.assertRaises(TypeError, adapter.getPath)
        self.assertRaises(TypeError, adapter.getRoot)

    def testWSideEffectDataInFront(self):
        provideAdapter(None, IPhysicallyLocatable, WrapperPhysicallyLocatable)
        provideAdapter(IContainmentRoot, IPhysicallyLocatable,
                       RootPhysicallyLocatable)

        root = Root()
        root = ContextWrapper(root, root, name='.',
                              side_effect_name="++skin++ZopeTop")
        f1 = ContextWrapper(C(), root, name='f1')
        f2 = ContextWrapper(C(),   f1, name='f2')
        f3 = ContextWrapper(C(),   f2, name='f3')

        adapter = getAdapter(f3, IPhysicallyLocatable)

        self.assertEqual(adapter.getPath(), '/f1/f2/f3')
        self.assertEqual(adapter.getRoot(), root)

        adapter = getAdapter(C(), IPhysicallyLocatable)
        self.assertRaises(TypeError, adapter.getPath)
        self.assertRaises(TypeError, adapter.getRoot)

    def testWSideEffectDataInMiddle(self):
        provideAdapter(None, IPhysicallyLocatable, WrapperPhysicallyLocatable)
        provideAdapter(IContainmentRoot, IPhysicallyLocatable,
                       RootPhysicallyLocatable)

        root = Root()
        c = C()
        f1 = ContextWrapper(c, root, name='f1')
        f1 = ContextWrapper(c, f1, name='.',
                            side_effect_name="++skin++ZopeTop")
        f2 = ContextWrapper(C(),   f1, name='f2')
        f3 = ContextWrapper(C(),   f2, name='f3')

        adapter = getAdapter(f3, IPhysicallyLocatable)

        self.assertEqual(adapter.getPath(), '/f1/f2/f3')
        self.assertEqual(adapter.getRoot(), root)

        adapter = getAdapter(C(), IPhysicallyLocatable)
        self.assertRaises(TypeError, adapter.getPath)
        self.assertRaises(TypeError, adapter.getRoot)

def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')
