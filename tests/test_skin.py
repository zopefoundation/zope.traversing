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
"""Test skin traversal.

$Id$
"""
from unittest import TestCase, main, makeSuite

class Test(TestCase):

    def test(self):
        from zope.app.traversing.namespace import skin

        class FauxRequest(object):
            def shiftNameToApplication(self):
                self.shifted = 1
            skin = ''
            def setPresentationSkin(self, skin):
                self.skin = skin

        request = FauxRequest()
        ob = object()
        ob2 = skin(ob, request).traverse('foo', ())
        self.assertEqual(ob, ob2)
        self.assertEqual(request.skin, 'foo')
        self.assertEqual(request.shifted, 1)

def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')
