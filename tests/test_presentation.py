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
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""

Revision information:
$Id: test_presentation.py,v 1.2 2002/12/25 14:13:27 jim Exp $
"""

from unittest import TestCase, TestSuite, main, makeSuite
from zope.app.tests.placelesssetup import PlacelessSetup
from zope.component.view import provideView
from zope.component.resource import provideResource
from zope.app.traversing.presentationnamespaces import view, resource
from zope.exceptions import NotFoundError
from zope.interface import Interface

class IContent(Interface): pass
class IPresentationType(Interface): pass

class Content: __implements__ = IContent

class Resource:

    def __init__(self, request): pass
    __implements__ = IPresentationType

class View:
    __implements__ = IPresentationType

    def __init__(self, content, request):
        self.content = content

class Request:

    def getPresentationType(self): return IPresentationType
    def getPresentationSkin(self): return ''


class Test(PlacelessSetup, TestCase):

    def testView(self):
        provideView(IContent, 'foo', IPresentationType, [View])

        ob = Content()
        v = view('foo', (), '@@foo', ob, Request())
        self.assertEqual(v.__class__, View)

    def testResource(self):
        provideResource('foo', IPresentationType, Resource)

        ob = Content()
        r = resource('foo', (), '++resource++foo', ob, Request())
        self.assertEqual(r.__class__, Resource)


def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')
