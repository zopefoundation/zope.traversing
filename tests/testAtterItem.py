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
$Id: testAtterItem.py,v 1.2 2002/06/10 23:28:17 jim Exp $
"""

from unittest import TestCase, TestSuite, main, makeSuite
from Zope.Testing.CleanUp import CleanUp # Base class w registry cleanup


class C:
    a = 1
    def __getitem__(self, key): return key+'value'
c=C()


class Test(CleanUp, TestCase):

    def testAttr(self):
        from Zope.App.Traversing.AttrItemNamespaces import attr
        self.assertEqual(attr('a', (), 'a;attribute', c, None), 1)

    def testItem(self):
        from Zope.App.Traversing.AttrItemNamespaces import item
        self.assertEqual(item('a', (), 'a;item', c, None), 'avalue')
        
        

def test_suite():
    return TestSuite((
        makeSuite(Test),
        ))

if __name__=='__main__':
    main(defaultTest='test_suite')
