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
$Id: test_atteritem.py,v 1.5 2004/04/17 17:15:35 jim Exp $
"""

from unittest import TestCase, main, makeSuite
from zope.testing.cleanup import CleanUp # Base class w registry cleanup


class C:
    a = 1
    def __getitem__(self, key): return key+'value'
c=C()


class Test(CleanUp, TestCase):

    def testAttr(self):
        from zope.app.traversing.namespace import attr
        self.assertEqual(attr('a', c, None), 1)

    def testItem(self):
        from zope.app.traversing.namespace import item
        self.assertEqual(item('a', c, None), 'avalue')



def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')
