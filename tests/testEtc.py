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
$Id: testEtc.py,v 1.4 2002/12/20 19:45:46 jim Exp $
"""

from unittest import TestCase, TestSuite, main, makeSuite
from Zope.Testing.CleanUp import CleanUp # Base class w registry cleanup

class Test(CleanUp, TestCase):

    def testApplicationControl(self):
        from Zope.App.Traversing.EtcNamespace import etc
        from Zope.App.OFS.ApplicationControl.ApplicationControl \
             import applicationController, applicationControllerRoot
        
        self.assertEqual(
            etc('ApplicationController', (), '++etc++ApplicationController',
                applicationControllerRoot, None),
            applicationController)

    def testServices(self):
        from Zope.App.Traversing.EtcNamespace import etc
        class C:
            def getServiceManager(self): return 42
        
        self.assertEqual(etc('Services', (), 'etc:Services', C(), None), 42)

        

def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')
