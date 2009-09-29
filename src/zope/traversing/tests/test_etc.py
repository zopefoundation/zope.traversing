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
"""Test 'etc' namespace

$Id$
"""
from unittest import TestCase, main, makeSuite
from zope.testing.cleanup import CleanUp # Base class w registry cleanup

class Test(CleanUp, TestCase):

    def testApplicationControl(self):
        # This test is to be taken with care. The 'process' name will only be
        # resolved if zope.app.applicationcontrol can be imported in the first
        # place. So there is no guarantee that 'process' can be resolved in
        # spite of the test; it just assures that if the applicationcontroller
        # can be imported, the 'process' name will be resolved correctly.
        # While the zope.traversing package itself no longer depends on
        # zope.app.applicationcontrol, its tests do, so we always test the
        # behaviour in the case that the application controller is present.

        import zope.component
        from zope.traversing.interfaces import IEtcNamespace
        from zope.traversing.namespace import etc
        from zope.app.applicationcontrol.applicationcontrol \
             import applicationController, applicationControllerRoot
        gsm = zope.component.getGlobalSiteManager()
        gsm.registerUtility(applicationController, IEtcNamespace, 'process')

        self.assertEqual(
            etc(applicationControllerRoot).traverse('process', ()),
            applicationController)

    def testSiteManager(self):
        from zope.traversing.namespace import etc
        class C(object):
            def getSiteManager(self): return 42

        self.assertEqual(etc(C()).traverse('site', ()), 42)



def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')