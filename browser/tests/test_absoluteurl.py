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
"""Test the AbsoluteURL view

$Id: test_absoluteurl.py,v 1.2 2004/03/15 20:42:10 jim Exp $
"""

from unittest import TestCase, main, makeSuite

from zope.app.tests import ztapi
from zope.interface import Interface, implements

from zope.app.tests.placelesssetup import PlacelessSetup
from zope.component import getService, getView

from zope.i18n.interfaces import IUserPreferredCharsets

from zope.publisher.browser import TestRequest
from zope.publisher.http import IHTTPRequest, HTTPCharsets
from zope.app.container.contained import contained


class IRoot(Interface): pass

class Root:
    implements(IRoot)

class TrivialContent(object):
    """Trivial content object, used because instances of object are rocks."""

class TestAbsoluteURL(PlacelessSetup, TestCase):

    def setUp(self):
        super(TestAbsoluteURL, self).setUp()
        from zope.app.traversing.browser import AbsoluteURL, SiteAbsoluteURL
        ztapi.browserView(None, 'absolute_url', AbsoluteURL)
        ztapi.browserView(IRoot, 'absolute_url', SiteAbsoluteURL)
        ztapi.provideAdapter(IHTTPRequest, IUserPreferredCharsets,
                             HTTPCharsets)

    def testBadObject(self):
        request = TestRequest()
        view = getView(42, 'absolute_url', request)
        self.assertRaises(TypeError, view.__str__)

    def testNoContext(self):
        request = TestRequest()
        view = getView(Root(), 'absolute_url', request)
        self.assertEqual(str(view), 'http://127.0.0.1')

    def testBasicContext(self):
        request = TestRequest()

        content = contained(TrivialContent(), Root(), name='a')
        content = contained(TrivialContent(), content, name='b')
        content = contained(TrivialContent(), content, name='c')
        view = getView(content, 'absolute_url', request)
        self.assertEqual(str(view), 'http://127.0.0.1/a/b/c')

        breadcrumbs = view.breadcrumbs()
        self.assertEqual(breadcrumbs,
                         ({'name':  '', 'url': 'http://127.0.0.1'},
                          {'name': 'a', 'url': 'http://127.0.0.1/a'},
                          {'name': 'b', 'url': 'http://127.0.0.1/a/b'},
                          {'name': 'c', 'url': 'http://127.0.0.1/a/b/c'},
                          ))

    def testVirtualHosting(self):
        request = TestRequest()

        vh_root = TrivialContent()
        content = contained(vh_root, Root(), name='a')
        request._vh_root = content
        content = contained(TrivialContent(), content, name='b')
        content = contained(TrivialContent(), content, name='c')
        view = getView(content, 'absolute_url', request)
        self.assertEqual(str(view), 'http://127.0.0.1/b/c')

        breadcrumbs = view.breadcrumbs()
        self.assertEqual(breadcrumbs,
         ({'name':  '', 'url': 'http://127.0.0.1'},
          {'name': 'b', 'url': 'http://127.0.0.1/b'},
          {'name': 'c', 'url': 'http://127.0.0.1/b/c'},
          ))

    def testVirtualHostingWithVHElements(self):
        request = TestRequest()

        vh_root = TrivialContent()
        content = contained(vh_root, Root(), name='a')
        request._vh_root = content
        content = contained(TrivialContent(), content, name='b')
        content = contained(TrivialContent(), content, name='c')
        view = getView(content, 'absolute_url', request)
        self.assertEqual(str(view), 'http://127.0.0.1/b/c')

        breadcrumbs = view.breadcrumbs()
        self.assertEqual(breadcrumbs,
         ({'name':  '', 'url': 'http://127.0.0.1'},
          {'name': 'b', 'url': 'http://127.0.0.1/b'},
          {'name': 'c', 'url': 'http://127.0.0.1/b/c'},
          ))

    def testVirtualHostingInFront(self):
        request = TestRequest()

        root = Root()
        request._vh_root = contained(root, root, name='')
        content = contained(root, None)
        content = contained(TrivialContent(), content, name='a')
        content = contained(TrivialContent(), content, name='b')
        content = contained(TrivialContent(), content, name='c')
        view = getView(content, 'absolute_url', request)
        self.assertEqual(str(view), 'http://127.0.0.1/a/b/c')

        breadcrumbs = view.breadcrumbs()
        self.assertEqual(breadcrumbs,
         ({'name':  '', 'url': 'http://127.0.0.1'},
          {'name': 'a', 'url': 'http://127.0.0.1/a'},
          {'name': 'b', 'url': 'http://127.0.0.1/a/b'},
          {'name': 'c', 'url': 'http://127.0.0.1/a/b/c'},
          ))


def test_suite():
    return makeSuite(TestAbsoluteURL)

if __name__=='__main__':
    main(defaultTest='test_suite')
