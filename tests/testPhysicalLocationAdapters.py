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
$Id: testPhysicalLocationAdapters.py,v 1.2 2002/07/13 14:18:36 jim Exp $
"""

from unittest import TestCase, TestSuite, main, makeSuite
from Zope.ComponentArchitecture.tests.PlacelessSetup import PlacelessSetup
from Zope.ComponentArchitecture.GlobalAdapterService import provideAdapter
from Zope.ComponentArchitecture import getAdapter

from Zope.App.Traversing.IContainmentRoot import IContainmentRoot
from Zope.App.Traversing.IPhysicallyLocatable import IPhysicallyLocatable
from Zope.App.Traversing.PhysicalLocationAdapters \
     import WrapperPhysicallyLocatable, RootPhysicallyLocatable
from Zope.Proxy.ContextWrapper import ContextWrapper

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
    return TestSuite((
        makeSuite(Test),
        ))

if __name__=='__main__':
    main(defaultTest='test_suite')





