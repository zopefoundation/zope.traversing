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

$Id: test_conveniencefunctions.py,v 1.18 2003/06/01 15:59:38 jim Exp $
"""
from unittest import TestCase, main, makeSuite
from zope.interface import directlyProvides
from zope.app.services.tests.placefulsetup import PlacefulSetup
from zope.app.context import ContextWrapper
from zope.context import isWrapper
from zope.app.traversing.adapters import Traverser
from zope.component import getService
from zope.app.services.servicenames import Adapters
from zope.app.interfaces.traversing import ITraverser, ITraversable
from zope.app.interfaces.traversing import IObjectName
from zope.app.traversing.adapters import DefaultTraversable, ObjectName

from zope.app.interfaces.traversing import IPhysicallyLocatable
from zope.app.interfaces.traversing import IContainmentRoot
from zope.app.traversing.adapters import WrapperPhysicallyLocatable
from zope.app.traversing.adapters import RootPhysicallyLocatable

from zope.security.proxy import Proxy
from zope.security.checker import selectChecker

from zope.exceptions import NotFoundError

class C:
    def __init__(self, name):
        self.name = name

def _proxied(*args):
    return Proxy(args, selectChecker(args))


class Test(PlacefulSetup, TestCase):

    def setUp(self):
        PlacefulSetup.setUp(self)
        # Build up a wrapper chain
        root = C('root')
        directlyProvides(root, IContainmentRoot)
        folder = C('folder')
        item = C('item')

        self.root = root  # root is not usually wrapped
        self.folder = ContextWrapper(folder, self.root,   name='folder')
        self.item =   ContextWrapper(item,   self.folder, name='item')
        self.unwrapped_item = item
        self.broken_chain_folder = ContextWrapper(folder, None)
        self.broken_chain_item = ContextWrapper(item,
                                    self.broken_chain_folder,
                                    name='item'
                                    )
        root.folder = folder
        folder.item = item

        self.tr = Traverser(root)
        getService(None, Adapters).provideAdapter(
              None, ITraverser, Traverser)
        getService(None, Adapters).provideAdapter(
              None, ITraversable, DefaultTraversable)
        getService(None, Adapters).provideAdapter(
              None, IObjectName, ObjectName)
        getService(None, Adapters).provideAdapter(
              None, IPhysicallyLocatable, WrapperPhysicallyLocatable)
        getService(None, Adapters).provideAdapter(
              IContainmentRoot, IPhysicallyLocatable, RootPhysicallyLocatable)


    def testTraverse(self):
        from zope.app.traversing import traverse
        self.assertEqual(
            traverse(self.item, '/folder/item'),
            self.tr.traverse('/folder/item')
            )

    def testTraverseFromUnwrapped(self):
        from zope.app.traversing import traverse
        self.assertRaises(
            TypeError,
            traverse,
            self.unwrapped_item, '/folder/item'
            )

    def testTraverseName(self):
        from zope.app.traversing import traverseName
        self.assertEqual(
            traverseName(self.folder, 'item'),
            self.tr.traverse('/folder/item')
            )
        self.assertEqual(
            traverseName(self.item, '.'),
            self.tr.traverse('/folder/item')
            )
        self.assertEqual(
            traverseName(self.item, '..'),
            self.tr.traverse('/folder')
            )
        self.assert_(isWrapper(traverseName(self.folder, 'item')))
        # XXX test that ++names++ and @@names work too

    def testTraverseNameBadValue(self):
        from zope.app.traversing import traverseName
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
        from zope.app.traversing import objectName
        self.assertEqual(
            objectName(self.item),
            'item'
            )

    def testObjectNameFromUnwrapped(self):
        from zope.app.traversing import objectName
        self.assertRaises(
            TypeError,
            objectName,
            self.unwrapped_item
            )

    def testGetParent(self):
        from zope.app.traversing import getParent
        self.assertEqual(
            getParent(self.item),
            self.folder
            )

    def testGetParentOtherContext(self):
        from zope.app.traversing import getParent
        item = ContextWrapper(self.item, self.root, name='item')
        self.assertEqual(
            getParent(item),
            self.folder
            )

    def testGetParentFromRoot(self):
        from zope.app.traversing import getParent
        self.assertEqual(
            getParent(self.root),
            None
            )

    def testGetParentBrokenChain(self):
        from zope.app.traversing import getParent
        self.assertRaises(
            TypeError,
            getParent,
            self.broken_chain_folder
            )

    def testGetParentFromUnwrapped(self):
        from zope.app.traversing import getParent
        self.assertRaises(
            TypeError,
            getParent,
            self.unwrapped_item
            )

    def testGetParents(self):
        from zope.app.traversing import getParents
        self.assertEqual(
            getParents(self.item),
            [self.folder, self.root]
            )

    def testGetParentsBrokenChain(self):
        from zope.app.traversing import getParents
        self.assertRaises(
            TypeError,
            getParents,
            self.broken_chain_item
            )

    def testGetParentsFromUnwrapped(self):
        from zope.app.traversing import getParents
        self.assertRaises(
            TypeError,
            getParents,
            self.unwrapped_item
            )

    def testGetParentFromUnwrapped(self):
        from zope.app.traversing import getParent
        self.assertRaises(
            TypeError,
            getParent,
            self.unwrapped_item
            )

    def testGetPhysicalPathString(self):
        from zope.app.traversing import getPath
        self.assertEqual(
            getPath(self.item),
            u'/folder/item'
            )

    def testGetPhysicalPathStringOfRoot(self):
        from zope.app.traversing import getPath
        self.assertEqual(
            getPath(self.root),
            u'/',
            )

    def testGetPhysicalRoot(self):
        from zope.app.traversing import getRoot
        self.assertEqual(
            getRoot(self.item),
            self.root
            )

    def testCanonicalPath(self):

        _bad_locations = (
            (UnicodeError, '\xa323'),
            (ValueError, ''),
            (ValueError, '//'),
            (ValueError, '/foo//bar'),

            # regarding the next two errors:
            # having a trailing slash on a location is undefined.
            # we might want to give it a particular meaning for zope3 later
            # for now, it is an invalid location identifier
            (ValueError, '/foo/bar/'),
            (ValueError, 'foo/bar/'),

            (IndexError, '/a/../..'),
            (ValueError, '/a//v'),
            )

        # sequence of N-tuples:
        #   (loc_returned_as_string, input, input, ...)
        # The string and tuple are tested as input as well as being the
        # specification for output.

        _good_locations = (
            # location returned as string
            ( u'/xx/yy/zz',
                # arguments to try in addition to the above
                '/xx/yy/zz',
                '/xx/./yy/ww/../zz',
            ),
            ( u'/xx/yy/zz',
                '/xx/yy/zz',
            ),
            ( u'/xx',
                '/xx',
            ),
            ( u'/',
                '/',
            ),
        )

        from zope.app.traversing import canonicalPath

        for error_type, value in _bad_locations:
            self.assertRaises(error_type, canonicalPath, value)

        for spec in _good_locations:
            correct_answer = spec[0]
            for argument in spec:
                self.assertEqual(canonicalPath(argument), correct_answer,
                                 "failure on %s" % argument)


    def test_normalizePath(self):

        _bad_locations = (
            (ValueError, '//'),
            (ValueError, '/foo//bar'),
            (IndexError, '/a/../..'),
            (IndexError, '/a/./../..'),
            )

        # sequence of N-tuples:
        #   (loc_returned_as_string, input, input, ...)
        # The string and tuple are tested as input as well as being the
        # specification for output.

        _good_locations = (
            # location returned as string
            ( '/xx/yy/zz',
              # arguments to try in addition to the above
              '/xx/yy/zz',
              '/xx/./yy/ww/../zz',
              '/xx/./yy/ww/./../zz',
            ),
            ( 'xx/yy/zz',
              # arguments to try in addition to the above
              'xx/yy/zz',
              'xx/./yy/ww/../zz',
              'xx/./yy/ww/./../zz',
            ),
            ( '/xx/yy/zz',
              '/xx/yy/zz',
            ),
            ( '/xx',
              '/xx',
            ),
            ( '/',
              '/',
            ),
        )


        from zope.app.traversing import _normalizePath

        for error_type, value in _bad_locations:
            self.assertRaises(error_type, _normalizePath, value)

        for spec in _good_locations:
            correct_answer = spec[0]
            for argument in spec:
                self.assertEqual(_normalizePath(argument), correct_answer,
                                 "failure on %s" % argument)

    def test_joinPath_slashes(self):
        from zope.app.traversing import joinPath
        path = u'/'
        args = ('/test', 'bla', '/foo', 'bar')
        self.assertRaises(ValueError, joinPath, path, *args)

        args = ('/test', 'bla', 'foo/', '/bar')
        self.assertRaises(ValueError, joinPath, path, *args)

    def test_joinPath(self):
        from zope.app.traversing import joinPath
        path = u'/bla'
        args = ('foo', 'bar', 'baz', 'bone')
        self.assertEqual(joinPath(path, *args), u'/bla/foo/bar/baz/bone')

        path = u'bla'
        args = ('foo', 'bar', 'baz', 'bone')
        self.assertEqual(joinPath(path, *args), u'bla/foo/bar/baz/bone')

        path = u'bla'
        args = ('foo', 'bar/baz', 'bone')
        self.assertEqual(joinPath(path, *args), u'bla/foo/bar/baz/bone')

        path = u'bla/'
        args = ('foo', 'bar', 'baz', 'bone')
        self.assertRaises(ValueError, joinPath, path, *args)

    def test_joinPath_normalize(self):
        from zope.app.traversing import joinPath
        path = u'/bla'
        args = ('foo', 'bar', '..', 'baz', 'bone')
        self.assertEqual(joinPath(path, *args), u'/bla/foo/baz/bone')

        path = u'bla'
        args = ('foo', 'bar', '.', 'baz', 'bone')
        self.assertEqual(joinPath(path, *args), u'bla/foo/bar/baz/bone')

        path = u'/'
        args = ('foo', 'bar', '.', 'baz', 'bone')
        self.assertEqual(joinPath(path, *args), u'/foo/bar/baz/bone')


def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')
