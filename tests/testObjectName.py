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
$Id: testObjectName.py,v 1.3 2002/10/04 18:37:24 jim Exp $
"""
from unittest import TestCase, TestSuite, main, makeSuite
from Interface import Interface

from Zope.App.tests.PlacelessSetup import PlacelessSetup
from Zope.ComponentArchitecture import getService, getAdapter

from Zope.Proxy.ContextWrapper import ContextWrapper

from Zope.App.Traversing.ObjectName \
    import IObjectName, ObjectName, SiteObjectName

class IRoot(Interface): pass

class Root:
    __implements__ = IRoot
    
class TrivialContent(object):
    """Trivial content object, used because instances of object are rocks."""

class Test(PlacelessSetup, TestCase):

    def setUp(self):
        PlacelessSetup.setUp(self)
                    
        provideAdapter = getService(None, "Adapters").provideAdapter
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

