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
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Physical Location Adapter Tests

$Id$
"""
from unittest import TestCase, main, makeSuite
from zope.app.tests.placelesssetup import PlacelessSetup
from zope.app.tests import ztapi
from zope.interface import implements

from zope.app.traversing.interfaces import IContainmentRoot
from zope.app.traversing.interfaces import IPhysicallyLocatable
from zope.app.location.traversing import LocationPhysicallyLocatable
from zope.app.traversing.adapters import RootPhysicallyLocatable
from zope.app.container.contained import contained
from zope.component.interfaces import IServiceService
from zope.app.site.servicecontainer import ServiceManagerContainer


class Root(object):
    implements(IContainmentRoot)

    __parent__ = None


class C(object):
    pass


class SiteManager(object):

    implements(IServiceService)

    def getService(self, object, name):
        '''See interface IServiceService'''
        raise ComponentLookupError(name)

    def getServiceDefinitions(self):
        '''See interface IServiceService'''
        return ()



class Test(PlacelessSetup, TestCase):

    def test(self):
        ztapi.provideAdapter(None, IPhysicallyLocatable,
                             LocationPhysicallyLocatable)
        ztapi.provideAdapter(IContainmentRoot, IPhysicallyLocatable,
                             RootPhysicallyLocatable)

        root = Root()
        f1 = contained(C(), root, name='f1')
        f2 = contained(ServiceManagerContainer(),   f1, name='f2')
        f3 = contained(C(),   f2, name='f3')
        
        adapter = IPhysicallyLocatable(f3)

        self.assertEqual(adapter.getPath(), '/f1/f2/f3')
        self.assertEqual(adapter.getName(), 'f3')
        self.assertEqual(adapter.getRoot(), root)
        self.assertEqual(adapter.getNearestSite(), root)

        f2.setSiteManager(SiteManager())
        self.assertEqual(adapter.getNearestSite(), f2)

        
def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')
