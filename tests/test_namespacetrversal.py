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
"""Traversal Namespace Tests

$Id: test_namespacetrversal.py,v 1.10 2004/04/17 17:15:35 jim Exp $
"""

from unittest import TestCase, main, makeSuite
from zope.testing.cleanup import CleanUp # Base class w registry cleanup
from zope.app.traversing.namespace import provideNamespaceHandler
from zope.app.traversing.namespace import attr, item
from zope.app.traversing.adapters import Traverser

class C:
    a = 1
    def __getitem__(self, key): return key+'value'

c=C()

def noop(name, ob, request):
    return ob


class Test(CleanUp, TestCase):

    def setUp(self):
        provideNamespaceHandler('attribute', attr)
        provideNamespaceHandler('item', item)
        provideNamespaceHandler('noop', noop)

    def testAttr(self):
        traverser = Traverser(c)
        v = traverser.traverse('++attribute++a')
        self.assertEqual(v, 1)

    def testItem(self):
        traverser = Traverser(c)
        v = traverser.traverse('++item++a')
        self.assertEqual(v, 'avalue')

    def testSideEffectsContextDetail(self):
        # Check to make sure that when we traverse something in context,
        # that we get the right context for the result.

        c = C()
        traverser = Traverser(c)
        v = traverser.traverse('++noop++yeeha')
        self.assert_(v is c)


def test_suite():
    suite = makeSuite(Test)
    from doctest import DocTestSuite
    suite.addTest(DocTestSuite('zope.app.traversing.namespace'))
    return suite




if __name__ == '__main__':
    main(defaultTest='test_suite')
