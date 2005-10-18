##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""Test lang traversal.

$Id$
"""

import unittest

from zope.interface import directlyProvides
from zope.publisher.interfaces.http import IHTTPRequest
from zope.i18n.interfaces import IModifiableUserPreferredLanguages

from zope.app.testing import ztapi
from zope.app.annotation import IAttributeAnnotatable, IAnnotations
from zope.app.annotation.attribute import AttributeAnnotations
from zope.app.publisher.browser import ModifiableBrowserLanguages
from zope.app.testing.placelesssetup import PlacelessSetup

from zope.app.traversing.namespace import lang


class TestRequest(dict):

    def __init__(self, languages):
        self["HTTP_ACCEPT_LANGUAGE"] = languages

    def setupLocale(self):
        self.localized = True

    def shiftNameToApplication(self):
        self.shifted = True

class Test(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(Test, self).setUp()
        self.request = TestRequest("en")
        directlyProvides(self.request, IHTTPRequest, IAttributeAnnotatable)
        ztapi.provideAdapter(IAttributeAnnotatable, IAnnotations,
            AttributeAnnotations)
        ztapi.provideAdapter(IHTTPRequest,
            IModifiableUserPreferredLanguages, ModifiableBrowserLanguages)

    def test_adapter(self):
        request = self.request
        browser_languages = IModifiableUserPreferredLanguages(request)
        self.failUnlessEqual(["en"], browser_languages.getPreferredLanguages())

        ob = object()
        ob2 = lang(ob, request).traverse('ru', ())
        self.failUnless(ob is ob2)
        self.failUnless(request.localized)
        self.failUnless(request.shifted)
        self.failUnlessEqual(["ru"], browser_languages.getPreferredLanguages())


def test_suite():
    return unittest.makeSuite(Test)

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')
