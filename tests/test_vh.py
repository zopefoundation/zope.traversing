##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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
"""Virtual hosting namespace tests.

$Id: test_vh.py,v 1.1 2003/04/15 09:37:27 alga Exp $
"""

import unittest

__metaclass__ = type

class TestRequest:

    def __init__(self, names=None, stack=None):
        self._traversal_stack = stack
        self._traversed_names = names
        self._app_server = 'http://server'
        self._app_url = ''

    def getTraversalStack(self):
        return list(self._traversal_stack)

    def setTraversalStack(self, stack):
        self._traversal_stack[:] = list(stack)

    def setApplicationNames(self, names):
        self._app_names = names

    def setApplicationServer(self, host, proto='http', port=None):
        host = "%s://%s" % (proto, host)
        if port:
            host = "%s:%s" % (host, port)
        self._app_server = host

    def setVirtualHostRoot(self):
        self._vh_trunc = len(self._traversed_names) + 1

class TestVHNamespace(unittest.TestCase):

    def test_vh(self):
        from zope.app.traversing.namespace import vh

        # GET /folder1/++vh++/x/y/z/++/folder1_1

        request = TestRequest(['folder1'], ['folder1_1', '++', 'z', 'y', 'x'])
        ob = object()
        result = vh('', (), '++vh++', ob, request)

        self.assertEqual(result, ob)
        self.assertEqual(request._traversal_stack, ['folder1_1'])
        #self.assertEqual(request._traversed_names, [])
        self.assertEqual(request._vh_trunc, 2)
        self.assertEqual(request._app_names, ['x', 'y', 'z'])
        self.assertEqual(request._app_server, 'http://server')

    def test_vh_noPlusPlus(self):
        from zope.app.traversing.namespace import vh

        # GET /folder1/folder2/++vh++http:host:80/folder1_1
        request = TestRequest(['folder1', 'folder2'], ['folder1_1'])
        ob = object()
        result = vh('http:host:80', (), '++vh++http:host:80', ob, request)

        self.assertEqual(result, ob)
        self.assertEqual(request._traversal_stack, ['folder1_1'])
        self.assertEqual(request._vh_trunc, 3)
        #self.assertEqual(request._traversed_names, [])
        self.assertEqual(request._app_names, [])

    def test_vh_host(self):
        from zope.app.traversing.namespace import vh

        request = TestRequest(['folder1'], ['folder1_1'])
        ob = object()
        result = vh('http:www.fubarco.com:80', (),
                    '++vh++http:www.fubarco.com:80', ob, request)

        self.assertEqual(request._app_server, 'http://www.fubarco.com:80')

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestVHNamespace))
    return suite


if __name__ == '__main__':
    unittest.main()
