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

$Id: testConvenienceFunctions.py,v 1.2 2002/06/18 22:14:16 stevea Exp $
"""
from unittest import TestCase, TestSuite, main, makeSuite
from Zope.App.OFS.Services.ServiceManager.tests.PlacefulSetup \
    import PlacefulSetup
from Zope.Proxy.ContextWrapper import ContextWrapper
from Zope.App.Traversing.Traverser import Traverser
from Zope.ComponentArchitecture import getService
from Zope.App.Traversing.ITraverser import ITraverser
from Zope.App.Traversing.ITraversable import ITraversable
from Zope.App.Traversing.DefaultTraversable import DefaultTraversable
from Zope.App.Traversing.ObjectName import IObjectName, ObjectName
from Zope.Exceptions import NotFoundError

class C:
    def __init__(self, name):
        self.name = name

class Test(PlacefulSetup, TestCase):

    def setUp(self):
        PlacefulSetup.setUp(self)
        # Build up a wrapper chain
        root = C('root')
        folder = C('folder')
        item = C('item')
        
        self.root =   ContextWrapper(root,   None,        name='')
        self.folder = ContextWrapper(folder, self.root,   name='folder')
        self.item =   ContextWrapper(item,   self.folder, name='item')
        self.unwrapped_item = item

        root.folder = folder
        folder.item = item

        self.tr = Traverser(root)
        getService(None,"Adapters").provideAdapter(
              None, ITraverser, Traverser)
        getService(None,"Adapters").provideAdapter(
              None, ITraversable, DefaultTraversable)
        getService(None,"Adapters").provideAdapter(
              None, IObjectName, ObjectName)


    def testTraverse(self):
        from Zope.App.Traversing import traverse
        self.assertEqual(
            traverse(self.item, '/folder/item'),
            self.tr.traverse('/folder/item')
            )
            
    def testTraverseFromUnwrapped(self):
        from Zope.App.Traversing import traverse
        self.assertRaises(
            TypeError,
            traverse,
            self.unwrapped_item, '/folder/item'
            )

    def testTraverseName(self):
        from Zope.App.Traversing import traverseName
        self.assertEqual(
            traverseName(self.folder, 'item'),
            self.tr.traverse('/folder/item')
            )
        self.assertEqual(
            traverseName(self.item, '.'),
            self.tr.traverse('/folder/item')
            )

            
    def testTraverseNameUnwrapped(self):
        from Zope.App.Traversing import traverseName
        self.assertRaises(
            TypeError,
            traverseName,
            self.unwrapped_item, 'item'
            )
            
    def testTraverseNameBadValue(self):
        from Zope.App.Traversing import traverseName
        self.assertRaises(
            NotFoundError,
            traverseName,
            self.folder, '../root'
            )
        self.assertRaises(
            NotFoundError,
            traverseName,
            self.folder, '/root'
            )
        self.assertRaises(
            NotFoundError,
            traverseName,
            self.folder, './item'
            )

    def testObjectName(self):
        from Zope.App.Traversing import objectName
        self.assertEqual(
            objectName(self.item),
            'item'
            )  

    def testObjectNameFromUnwrapped(self):
        from Zope.App.Traversing import objectName
        self.assertRaises(
            TypeError,
            objectName,
            self.unwrapped_item
            )  

    def testGetParent(self):
        from Zope.App.Traversing import getParent
        self.assertEqual(
            getParent(self.item),
            self.folder
            )  

    def testGetParentFromUnwrapped(self):
        from Zope.App.Traversing import getParent
        self.assertRaises(
            TypeError,
            getParent,
            self.unwrapped_item
            )  

    def testGetParents(self):
        from Zope.App.Traversing import getParents
        self.assertEqual(
            getParents(self.item),
            [self.folder, self.root]
            )

    def testGetParentsFromUnwrapped(self):
        from Zope.App.Traversing import getParents
        self.assertRaises(
            TypeError,
            getParents,
            self.unwrapped_item
            )

    def testGetPhysicalPath(self):
        from Zope.App.Traversing import getPhysicalPath
        self.assertEqual(
            getPhysicalPath(self.item),
            ('', 'folder', 'item')
            )

    def testGetPhysicalPathFromUnwrapped(self):
        from Zope.App.Traversing import getPhysicalPath
        self.assertRaises(
            TypeError,
            getPhysicalPath,
            self.unwrapped_item
            )

    def testGetPhysicalRoot(self):
        from Zope.App.Traversing import getPhysicalRoot
        self.assertEqual(
            getPhysicalRoot(self.item),
            self.root
            )

    def testGetPhysicalRootFromUnwrapped(self):
        from Zope.App.Traversing import getPhysicalRoot
        self.assertRaises(
            TypeError,
            getPhysicalRoot,
            self.unwrapped_item
            )

def test_suite():
    return TestSuite((
        makeSuite(Test),
        ))

if __name__=='__main__':
    main(defaultTest='test_suite')
