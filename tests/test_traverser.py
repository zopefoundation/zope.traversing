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

$Id: test_traverser.py,v 1.10 2003/05/27 14:18:27 jim Exp $
"""

import unittest

from zope.interface import directlyProvides
from zope.interface.verify import verifyClass
from zope.interface.implements import instancesOfObjectImplements

from zope.app.interfaces.traversing import ITraverser, ITraversable
from zope.app.traversing.adapters import Traverser, DefaultTraversable

from zope.app.interfaces.traversing import IPhysicallyLocatable
from zope.app.interfaces.traversing import IContainmentRoot
from zope.app.traversing.adapters import WrapperPhysicallyLocatable
from zope.app.traversing.adapters import RootPhysicallyLocatable

from zope.context import ContextWrapper
from zope.exceptions import NotFoundError, Unauthorized
from zope.component import getService
from zope.app.services.servicenames import Adapters

from zope.app.services.tests.placefulsetup import PlacefulSetup
from zope.security.checker \
    import ProxyFactory, defineChecker, CheckerPublic, Checker
from zope.security.management import newSecurityManager

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
        directlyProvides(self.root, IContainmentRoot)
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

        getService(None, Adapters).provideAdapter(
              None, ITraversable, DefaultTraversable)
        getService(None, Adapters).provideAdapter(
              None, IPhysicallyLocatable, WrapperPhysicallyLocatable)
        getService(None, Adapters).provideAdapter(
              IContainmentRoot, IPhysicallyLocatable, RootPhysicallyLocatable)

        self.root = root = C('root')
        directlyProvides(self.root, IContainmentRoot)
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

        getService(None,Adapters).provideAdapter(
             None, ITraversable, DefaultTraversable)
        getService(None, Adapters).provideAdapter(
              None, IPhysicallyLocatable, WrapperPhysicallyLocatable)
        getService(None, Adapters).provideAdapter(
              IContainmentRoot, IPhysicallyLocatable, RootPhysicallyLocatable)

        self.root = root = C('root')
        directlyProvides(root, IContainmentRoot)
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
