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

$Id: test_vh.py,v 1.2 2003/08/08 18:07:55 jim Exp $
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

    def setApplicationServer(self, host, proto='http', port=None):
        host = "%s://%s" % (proto, host)
        if port:
            host = "%s:%s" % (host, port)
        self._app_server = host

    def setVirtualHostRoot(self, names=None):
        del self._traversed_names[:]
        self._app_names = names or []

class TestVHNamespace(unittest.TestCase):

    def test_vh(self):
        from zope.app.traversing.namespace import vh

        # GET /folder1/++vh++/x/y/z/++/folder1_1

        request = TestRequest(['folder1'], ['folder1_1', '++', 'z', 'y', 'x'])
        ob = object()
        result = vh('', (), '++vh++', ob, request)

        self.assertEqual(result, ob)
        self.assertEqual(request._traversal_stack, ['folder1_1'])
        self.assertEqual(request._traversed_names, [])
        self.assertEqual(request._app_names, ['x', 'y', 'z'])
        self.assertEqual(request._app_server, 'http://server')

    def test_vh_noPlusPlus(self):
        from zope.app.traversing.namespace import vh

        # GET /folder1/folder2/++vh++http:host:80/folder1_1
        request = TestRequest(['folder1', 'folder2'], ['folder1_1'])
        ob = object()
        self.assertRaises(ValueError, vh,
                          'http:host:80', (), '++vh++http:host:80', ob, request)


    def test_vh_host(self):
        from zope.app.traversing.namespace import vh

        request = TestRequest(['folder1'], ['folder1_1', '++'])
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