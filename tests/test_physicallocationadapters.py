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
$Id: test_physicallocationadapters.py,v 1.2 2002/12/25 14:13:27 jim Exp $
"""

from unittest import TestCase, TestSuite, main, makeSuite
from zope.app.tests.placelesssetup import PlacelessSetup
from zope.component.adapter import provideAdapter
from zope.component import getAdapter

from zope.app.interfaces.traversing.containmentroot import IContainmentRoot
from zope.app.interfaces.traversing.physicallylocatable import IPhysicallyLocatable
from zope.app.traversing.physicallocationadapters \
     import WrapperPhysicallyLocatable, RootPhysicallyLocatable
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

        self.assertEqual(adapter.getPhysicalPath(), ('', 'f1', 'f2', 'f3'))
        self.assertEqual(adapter.getPhysicalRoot(), root)

        adapter = getAdapter(C(), IPhysicallyLocatable)
        self.assertRaises(TypeError, adapter.getPhysicalPath)
        self.assertRaises(TypeError, adapter.getPhysicalRoot)

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

        self.assertEqual(adapter.getPhysicalPath(), ('', 'f1', 'f2', 'f3'))
        self.assertEqual(adapter.getPhysicalRoot(), root)

        adapter = getAdapter(C(), IPhysicallyLocatable)
        self.assertRaises(TypeError, adapter.getPhysicalPath)
        self.assertRaises(TypeError, adapter.getPhysicalRoot)

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

        self.assertEqual(adapter.getPhysicalPath(), ('', 'f1', 'f2', 'f3'))
        self.assertEqual(adapter.getPhysicalRoot(), root)

        adapter = getAdapter(C(), IPhysicallyLocatable)
        self.assertRaises(TypeError, adapter.getPhysicalPath)
        self.assertRaises(TypeError, adapter.getPhysicalRoot)

def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')
