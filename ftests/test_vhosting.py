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
"""Functional tests for virtual hosting.

$Id: test_vhosting.py,v 1.2 2003/04/15 12:24:34 alga Exp $
"""

import unittest
from zope.testing.functional import BrowserTestCase
from zope.app.content.zpt import ZPTPage
from zope.app.content.folder import Folder
from transaction import get_transaction
from zope.component.resource import provideResource
from zope.publisher.interfaces.browser import IBrowserPresentation
from zope.app.publisher.browser.resource import Resource

class TestVirtualHosting(BrowserTestCase):

    def test_request_url(self):
        self.addPage('/pt', u'<span tal:replace="request/URL"/>')
        self.verify('/pt', 'http://localhost/pt/index.html\n')
        self.verify('/++vh++/pt',
                    'http://localhost/pt/index.html\n')
        self.verify('/++vh++https:otherhost:443/pt',
                    'https://otherhost:443/pt/index.html\n')
        self.verify('/++vh++https:otherhost:443/fake/folders/++/pt',
                    'https://otherhost:443/fake/folders/pt/index.html\n')

        self.addPage('/foo/bar/pt', u'<span tal:replace="request/URL"/>')
        self.verify('/foo/bar/pt', 'http://localhost/foo/bar/pt/index.html\n')
        self.verify('/foo/bar/++vh++/pt',
                    'http://localhost/pt/index.html\n')
        self.verify('/foo/bar/++vh++https:otherhost:443/pt',
                    'https://otherhost:443/pt/index.html\n')
        self.verify('/foo/++vh++https:otherhost:443/fake/folders/++/bar/pt',
                    'https://otherhost:443/fake/folders/bar/pt/index.html\n')

    def test_request_base(self):
        self.addPage('/pt', u'<head></head>')
        self.verify('/pt',
                    '<head>\n<base href="http://localhost/pt/index.html" />\n'
                    '</head>\n')
        self.verify('/++vh++/pt',
                    '<head>\n<base href="http://localhost/pt/index.html" />\n'
                    '</head>\n')
        self.verify('/++vh++https:otherhost:443/pt',
                    '<head>\n'
                    '<base href="https://otherhost:443/pt/index.html" />'
                    '\n</head>\n')
        self.verify('/++vh++https:otherhost:443/fake/folders/++/pt',
                    '<head>\n<base href='
                    '"https://otherhost:443/fake/folders/pt/index.html" />'
                    '\n</head>\n')

        self.addPage('/foo/bar/pt', u'<head></head>')
        self.verify('/foo/bar/pt',
                    '<head>\n<base '
                    'href="http://localhost/foo/bar/pt/index.html" />\n'
                    '</head>\n')
        self.verify('/foo/bar/++vh++/pt',
                    '<head>\n<base href="http://localhost/pt/index.html" />\n'
                    '</head>\n')
        self.verify('/foo/bar/++vh++https:otherhost:443/pt',
                    '<head>\n'
                    '<base href="https://otherhost:443/pt/index.html" />'
                    '\n</head>\n')
        self.verify('/foo/++vh++https:otherhost:443/fake/folders/++/bar/pt',
                    '<head>\n<base href='
                    '"https://otherhost:443/fake/folders/bar/pt/index.html" />'
                    '\n</head>\n')

    def test_absolute_url(self):
        self.addPage('/pt', u'<span tal:replace="template/@@absolute_url"/>')
        self.verify('/pt', 'http://localhost/pt\n')
        self.verify('/++vh++/pt',
                    'http://localhost/pt\n')
        self.verify('/++vh++https:otherhost:443/pt',
                    'https://otherhost:443/pt\n')
        self.verify('/++vh++https:otherhost:443/fake/folders/++/pt',
                    'https://otherhost:443/fake/folders/pt\n')

        self.addPage('/foo/bar/pt',
                     u'<span tal:replace="template/@@absolute_url"/>')
        self.verify('/foo/bar/pt', 'http://localhost/foo/bar/pt\n')
        self.verify('/foo/bar/++vh++/pt',
                    'http://localhost/pt\n')
        self.verify('/foo/bar/++vh++https:otherhost:443/pt',
                    'https://otherhost:443/pt\n')
        self.verify('/foo/++vh++https:otherhost:443/fake/folders/++/bar/pt',
                    'https://otherhost:443/fake/folders/bar/pt\n')

    def test_resources(self):
        provideResource('quux', IBrowserPresentation, Resource)
        self.addPage('/foo/bar/pt',
                     u'<span tal:replace="context/@@/quux" />')
        self.verify('/foo/bar/pt', '/@@/quux\n')
        self.verify('/foo/++vh++https:otherhost:443/fake/folders/++/bar/pt',
                    '/fake/folders/@@/quux\n')

    def createFolders(self, path):
        """addFolders('/a/b/c/d') would traverse and/or create three nested
        folders (a, b, c) and return a tuple (c, 'd') where c is a Folder
        instance at /a/b/c."""
        folder = self.getRootFolder()
        if path[0] == '/':
            path = path[1:]
        path = path.split('/')
        for id in path[:-1]:
            try:
                folder = folder[id]
            except KeyError:
                folder.setObject(id, Folder())
                folder = folder[id]
        return folder, path[-1]

    def addPage(self, path, content):
        folder, id = self.createFolders(path)
        page = ZPTPage()
        page.source = content
        folder.setObject(id, page)
        get_transaction().commit()

    def verify(self, path, content):
        result = self.publish(path)
        self.assertEquals(result.getStatus(), 200)
        self.assertEquals(result.getBody(), content)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestVirtualHosting))
    return suite


if __name__ == '__main__':
    unittest.main()
