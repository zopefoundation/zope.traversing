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
"""Test the ObjectName adapter

Revision information:
$Id: test_objectname.py,v 1.6 2003/02/12 02:17:40 seanb Exp $
"""
from unittest import TestCase, TestSuite, main, makeSuite
from zope.interface import Interface

from zope.app.tests.placelesssetup import PlacelessSetup
from zope.component import getService, getAdapter
from zope.app.services.servicenames import Adapters

from zope.proxy.context import ContextWrapper
from zope.app.interfaces.traversing import IObjectName
from zope.app.traversing.adapters import ObjectName, SiteObjectName

class IRoot(Interface): pass

class Root:
    __implements__ = IRoot

class TrivialContent(object):
    """Trivial content object, used because instances of object are rocks."""

class Test(PlacelessSetup, TestCase):

    def setUp(self):
        PlacelessSetup.setUp(self)

        provideAdapter = getService(None, Adapters).provideAdapter
        provideAdapter(None, IObjectName, [ObjectName])
        provideAdapter(IRoot, IObjectName, [ObjectName])

    def testAdapterBadObject(self):
        adapter = getAdapter(None, IObjectName)
        self.assertRaises(TypeError, adapter)

    def testAdapterNoContext(self):
        adapter = getAdapter(Root(), IObjectName)
        self.assertRaises(TypeError, adapter)

    def testAdapterBasicContext(self):
        content = ContextWrapper(TrivialContent(), Root(), name='a')
        content = ContextWrapper(TrivialContent(), content, name='b')
        content = ContextWrapper(TrivialContent(), content, name='c')
        adapter = getAdapter(content, IObjectName)
        self.assertEqual(adapter(), 'c')

def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')
