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

$Id: testConvenienceFunctions.py,v 1.4 2002/07/11 18:21:34 jim Exp $
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

from Zope.App.Traversing.IPhysicallyLocatable import IPhysicallyLocatable
from Zope.App.Traversing.IContainmentRoot import IContainmentRoot
from Zope.App.Traversing.PhysicalLocationAdapters \
     import WrapperPhysicallyLocatable, RootPhysicallyLocatable


from Zope.Exceptions import NotFoundError

class C:
    def __init__(self, name):
        self.name = name

class Test(PlacefulSetup, TestCase):

    def setUp(self):
        PlacefulSetup.setUp(self)
        # Build up a wrapper chain
        root = C('root')
        root.__implements__ = IContainmentRoot
        folder = C('folder')
        item = C('item')
        
        self.root =   root
        self.folder = ContextWrapper(folder, self.root,   name='folder')
        self.item =   ContextWrapper(item,   self.folder, name='item')
        self.unwrapped_item = item

        root.folder = folder
        folder.item = item

        self.tr = Traverser(root)
        getService(None, "Adapters").provideAdapter(
              None, ITraverser, Traverser)
        getService(None, "Adapters").provideAdapter(
              None, ITraversable, DefaultTraversable)
        getService(None, "Adapters").provideAdapter(
              None, IObjectName, ObjectName)
        getService(None, "Adapters").provideAdapter(
              None, IPhysicallyLocatable, WrapperPhysicallyLocatable)
        getService(None, "Adapters").provideAdapter(
              IContainmentRoot, IPhysicallyLocatable, RootPhysicallyLocatable)


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

    def testLocationAsTuple(self):
        # TODO: put these assertions in a less random order
        from Zope.App.Traversing import locationAsTuple as lat
        loc = (u'xx',u'yy',u'zz')
        self.assertEqual(lat((u'xx',u'yy',u'zz')), loc)
        self.assertEqual(lat((u'', u'xx',u'yy',u'zz')), (u'',)+loc)
        self.assertEqual(lat(('xx','yy','zz')), loc)
        self.assertRaises(ValueError, lat, ())
        self.assertEqual(lat(('xx',)), (u'xx',))
        self.assertRaises(ValueError, lat, 23)
        self.assertRaises(UnicodeError, lat, ('', u'123', '£23'))
        self.assertRaises(UnicodeError, lat, '£23')
        self.assertEqual(lat(u'xx/yy/zz'), loc)
        self.assertEqual(lat(u'/xx/yy/zz'), (u'',)+loc)
        self.assertEqual(lat('xx/yy/zz'), loc)
        self.assertRaises(ValueError, lat, '')
        self.assertEqual(lat('/'), (u'',))
        self.assertEqual(lat('xx'), (u'xx',))
        self.assertRaises(ValueError, lat, '//')
        self.assertRaises(AssertionError, lat, '/foo//bar')
        # having a trailing slash on a location is undefined.
        # we might want to give it a particular meaning for zope3 later
        # for now, it is an invalid location identifier
        self.assertRaises(ValueError, lat, '/foo/bar/')
        self.assertRaises(ValueError, lat, 'foo/bar/')
        self.assertRaises(ValueError, lat, ('','foo','bar',''))
        self.assertRaises(ValueError, lat, ('foo','bar',''))
        
    def testLocationAsUnicode(self):
        from Zope.App.Traversing import locationAsUnicode as lau
        loc = u'xx/yy/zz'
        self.assertEqual(lau((u'xx',u'yy',u'zz')), loc)
        self.assertEqual(lau((u'', u'xx',u'yy',u'zz')), '/'+loc)
        self.assertEqual(lau(('xx','yy','zz')), loc)
        self.assertRaises(ValueError, lau, ())
        self.assertEqual(lau(('xx',)), u'xx')
        self.assertRaises(ValueError, lau, 23)
        self.assertRaises(UnicodeError, lau, ('', u'123', '£23'))
        self.assertRaises(UnicodeError, lau, '£23')
        self.assertEqual(lau(u'xx/yy/zz'), loc)
        self.assertEqual(lau(u'/xx/yy/zz'), u'/'+loc)
        self.assertEqual(lau('xx/yy/zz'), loc)
        self.assertRaises(ValueError, lau, '')
        self.assertEqual(lau('/'), u'/')
        self.assertEqual(lau('xx'), u'xx')
        self.assertRaises(ValueError, lau, '//')
        self.assertRaises(AssertionError, lau, '/foo//bar')
        # having a trailing slash on a location is undefined.
        # we might want to give it a particular meaning for zope3 later
        # for now, it is an invalid location identifier
        self.assertRaises(ValueError, lau, '/foo/bar/')
        self.assertRaises(ValueError, lau, 'foo/bar/')
        self.assertRaises(ValueError, lau, ('','foo','bar',''))
        self.assertRaises(ValueError, lau, ('foo','bar',''))

def test_suite():
    return TestSuite((
        makeSuite(Test),
        ))

if __name__=='__main__':
    main(defaultTest='test_suite')
