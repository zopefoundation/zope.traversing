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

$Id: testTraverser.py,v 1.4 2002/07/11 18:21:34 jim Exp $
"""

import unittest
from Zope.App.Traversing.ITraverser import ITraverser
from Zope.App.Traversing.ITraversable import ITraversable
from Zope.App.Traversing.Traverser import Traverser
from Zope.App.Traversing.DefaultTraversable import DefaultTraversable

from Zope.App.Traversing.IPhysicallyLocatable import IPhysicallyLocatable
from Zope.App.Traversing.IContainmentRoot import IContainmentRoot
from Zope.App.Traversing.PhysicalLocationAdapters \
     import WrapperPhysicallyLocatable, RootPhysicallyLocatable

from Zope.Proxy.ContextWrapper import ContextWrapper
from Zope.Exceptions import NotFoundError, Unauthorized
from Zope.ComponentArchitecture import getService
from Zope.Security.SecurityManagement \
    import setSecurityPolicy, noSecurityManager

from Interface.Verify import verifyClass
from Interface.Implements import instancesOfObjectImplements
from Zope.App.OFS.Services.ServiceManager.tests.PlacefulSetup \
    import PlacefulSetup
from Zope.Security.Checker \
    import ProxyFactory, defineChecker, NamesChecker, CheckerPublic, Checker
from Zope.Security.SecurityManagement import newSecurityManager

class C:
    def __init__(self, name):
        self.name = name

class TraverserTests(PlacefulSetup, unittest.TestCase):

    def setUp(self):
        PlacefulSetup.setUp(self)
        # Build up a wrapper chain
        self.root =   C('root')
        self.folder = ContextWrapper(C('folder'), self.root,   name='folder')
        self.item =   ContextWrapper(C('item'),   self.folder, name='item')
        self.tr = Traverser(self.item)

    def testImplementsITraverser(self):
        self.failUnless(ITraverser.isImplementedBy(self.tr))

    def testVerifyInterfaces(self):
        for interface in instancesOfObjectImplements(Traverser):
            verifyClass(interface, Traverser)

class UnrestrictedNoTraverseTests(unittest.TestCase):
    def setUp(self):
        self.root = root = C('root')
        self.root.__implements__ = IContainmentRoot
        self.folder = folder = C('folder')
        self.item = item = C('item')

        root.folder = folder
        folder.item = item

        self.tr = Traverser(root)

    def testNoTraversable(self):
        self.assertRaises(NotFoundError, self.tr.traverse,
                          'folder')

class UnrestrictedTraverseTests(PlacefulSetup, unittest.TestCase):
    def setUp(self):
        PlacefulSetup.setUp(self)
        # Build up a wrapper chain

        getService(None, "Adapters").provideAdapter(
              None, ITraversable, DefaultTraversable)
        getService(None, "Adapters").provideAdapter(
              None, IPhysicallyLocatable, WrapperPhysicallyLocatable)
        getService(None, "Adapters").provideAdapter(
              IContainmentRoot, IPhysicallyLocatable, RootPhysicallyLocatable)

        self.root = root = C('root')
        self.root.__implements__ = IContainmentRoot
        self.folder = folder = C('folder')
        self.item = item = C('item')

        root.folder = folder
        folder.item = item

        self.tr = Traverser(root)

    def testSimplePathString(self):
        tr = self.tr
        item = self.item

        self.assertEquals(tr.traverse('/folder/item'), item)
        self.assertEquals(tr.traverse('folder/item'), item)
        self.assertEquals(tr.traverse('/folder/item/'), item)

    def testSimplePathUnicode(self):
        tr = self.tr
        item = self.item

        self.assertEquals(tr.traverse(u'/folder/item'), item)
        self.assertEquals(tr.traverse(u'folder/item'), item)
        self.assertEquals(tr.traverse(u'/folder/item/'), item)

    def testSimplePathTuple(self):
        tr = self.tr
        item = self.item

        self.assertEquals(tr.traverse(('', 'folder', 'item')),
                          item)
        self.assertEquals(tr.traverse(('folder', 'item')), item)

    def testComplexPathString(self):
        tr = self.tr
        item = self.item

        self.assertEquals(tr.traverse('/folder/../folder/./item'),
            item)
        self.assertEquals(tr.traverse(
            '/../folder/../../folder/item'), item)
        self.assertEquals(tr.traverse('../../folder/item'), item)

    def testNotFoundDefault(self):
        self.assertEquals(self.tr.traverse('foo', 'notFound'),
            'notFound')

    def testNotFoundNoDefault(self):
        self.assertRaises(NotFoundError, self.tr.traverse, 'foo')

def Denied(*names):

    def check(name):
        if name in names:
            return 'Waaaa'
        return CheckerPublic

    return Checker(check)

class RestrictedTraverseTests(PlacefulSetup, unittest.TestCase):
    _oldPolicy = None
    _deniedNames = ()

    def setUp(self):
        PlacefulSetup.setUp(self)

        getService(None,"Adapters").provideAdapter(
             None, ITraversable, DefaultTraversable)
        getService(None, "Adapters").provideAdapter(
              None, IPhysicallyLocatable, WrapperPhysicallyLocatable)
        getService(None, "Adapters").provideAdapter(
              IContainmentRoot, IPhysicallyLocatable, RootPhysicallyLocatable)

        self.root = root = C('root')
        root.__implements__ = IContainmentRoot
        self.folder = folder = C('folder')
        self.item = item = C('item')

        root.folder = folder
        folder.item = item

        self.tr = Traverser(ProxyFactory(root))

    def testAllAllowed(self):
        defineChecker(C, Checker(lambda name: CheckerPublic)) 
        tr = Traverser(ProxyFactory(self.root))
        item = self.item

        self.assertEquals(tr.traverse(('', 'folder', 'item')), item)
        self.assertEquals(tr.traverse(('folder', 'item')), item)
        
    def testItemDenied(self):
        newSecurityManager('no one')
        defineChecker(C, Denied('item')) 
        tr = Traverser(ProxyFactory(self.root))
        folder = self.folder

        self.assertRaises(Unauthorized, tr.traverse, 
            ('', 'folder', 'item'))
        self.assertRaises(Unauthorized, tr.traverse, 
            ('folder', 'item'))
        self.assertEquals(tr.traverse(('', 'folder')), folder)
        self.assertEquals(tr.traverse(('folder', '..', 'folder')),
                          folder)
        self.assertEquals(tr.traverse(('folder',)), folder)

class DefaultTraversableTests(unittest.TestCase):
    def testImplementsITraversable(self):
        self.failUnless(ITraversable.isImplementedBy(DefaultTraversable(None)))

    def testVerifyInterfaces(self):
        for interface in instancesOfObjectImplements(DefaultTraversable):
            verifyClass(interface, DefaultTraversable)

    def testAttributeTraverse(self):
        root = C('root')
        item = C('item')
        root.item = item
        df = DefaultTraversable(root)

        further = []
        next = df.traverse('item', (), 'item', further)
        self.failUnless(next is item)
        self.assertEquals(further, [])

    def testDictionaryTraverse(self):
        dict = {}
        foo = C('foo')
        dict['foo'] = foo
        df = DefaultTraversable(dict)

        further = []
        next = df.traverse('foo', (), 'foo', further)
        self.failUnless(next is foo)
        self.assertEquals(further, [])

    def testNotFound(self):
        df = DefaultTraversable(C('dummy'))

        self.assertRaises(NotFoundError, df.traverse, 'bar', (), 'bar', [])

def test_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TraverserTests)
    suite.addTest(loader.loadTestsFromTestCase(DefaultTraversableTests))
    suite.addTest(loader.loadTestsFromTestCase(UnrestrictedNoTraverseTests))
    suite.addTest(loader.loadTestsFromTestCase(UnrestrictedTraverseTests))
    suite.addTest(loader.loadTestsFromTestCase(RestrictedTraverseTests))
    return suite

if __name__=='__main__':
    unittest.TextTestRunner().run(test_suite())
