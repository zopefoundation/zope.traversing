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
$Id: testSkin.py,v 1.2 2002/07/17 16:54:20 jeremy Exp $
"""

from unittest import TestCase, TestSuite, main, makeSuite
from Zope.Testing.CleanUp import CleanUp # Base class w registry cleanup
from Zope.Publisher.Browser.BrowserRequest import TestRequest

class Test(CleanUp, TestCase):

    def test(self):
        from Zope.App.Traversing.SkinNamespace import skin

        request = TestRequest()
        self.assertEqual(request.getPresentationSkin(), '')
        ob = object()
        ob2 = skin('foo', (), '++skin++foo', ob, request)
        self.assertEqual(ob, ob2)
        self.assertEqual(request.getPresentationSkin(), 'foo')

def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')
