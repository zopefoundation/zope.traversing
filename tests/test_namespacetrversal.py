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
$Id: test_namespacetrversal.py,v 1.4 2003/05/01 19:35:38 faassen Exp $
"""

from unittest import TestCase, main, makeSuite
from zope.testing.cleanup import CleanUp # Base class w registry cleanup

class C:
    a = 1
    def __getitem__(self, key): return key+'value'

c=C()


class Test(CleanUp, TestCase):

    def setUp(self):
        from zope.app.traversing.namespace import provideNamespaceHandler
        from zope.app.traversing.namespace import attr, item
        from zope.app.traversing.namespace import skin
        provideNamespaceHandler('attribute', attr)
        provideNamespaceHandler('item', item)
        provideNamespaceHandler('skin', skin)

    def testAttr(self):
        from zope.app.traversing.adapters import Traverser
        traverser = Traverser(c)
        v = traverser.traverse('++attribute++a')
        self.assertEqual(v, 1)

    def testItem(self):
        from zope.app.traversing.adapters import Traverser
        traverser = Traverser(c)
        v = traverser.traverse('++item++a')
        self.assertEqual(v, 'avalue')

    def testSideEffectsContextDetail(self):
        # Check to make sure that when we traverse something in context,
        # that we get the right context for the result.
        from zope.proxy.context import ContextWrapper, getWrapperContainer
        from zope.app.traversing.adapters import Traverser
        from zope.publisher.browser import TestRequest

        c1 = C()
        c2 = C()
        c2c1 = ContextWrapper(c2, c1)

        traverser = Traverser(c2c1)
        v = traverser.traverse('++skin++ZopeTop', request=TestRequest())
        self.assertEqual(v, c2)
        self.failUnless(getWrapperContainer(v) is c2c1)


def test_suite():
    return makeSuite(Test)


if __name__ == '__main__':
    main(defaultTest='test_suite')
