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
$Id: testAcquire.py,v 1.3 2002/07/17 16:54:20 jeremy Exp $
"""

from unittest import TestCase, TestSuite, main, makeSuite
from Zope.ComponentArchitecture.tests.PlacelessSetup import PlacelessSetup
from Zope.App.Traversing.ITraversable import ITraversable
from Zope.App.Traversing.DefaultTraversable import DefaultTraversable
from Zope.ComponentArchitecture.GlobalAdapterService import provideAdapter
from Zope.Proxy.ContextWrapper import ContextWrapper, getWrapperContext
from Zope.App.Traversing.AcquireNamespace import acquire
from Zope.Exceptions import NotFoundError

class Test(PlacelessSetup, TestCase):

    def test(self):
        provideAdapter(None, ITraversable, DefaultTraversable)

        class C:
            def __init__(self, name):
                self.name = name

        a = C('a')
        a.a1 = C('a1')
        a.a2 = C('a2')
        a.a2.a21 = C('a21')
        a.a2.a21.a211 = C('a211')

        a2 = ContextWrapper(a.a2, a)
        a21 = ContextWrapper(a.a2.a21, a2)
        a211 = ContextWrapper(a.a2.a21.a211, a21)

        acquired = acquire('a1', (), 'a1;acquire', a211, None)

        self.assertEqual(acquired.name, 'a1')

        self.assertRaises(NotFoundError,
                          acquire, 'a3', (), 'a1;acquire', a211, None)
        
        

def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')
