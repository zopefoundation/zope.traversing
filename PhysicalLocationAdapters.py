##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
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
"""XXX short summary goes here.

XXX longer description goes here.

$Id: PhysicalLocationAdapters.py,v 1.2 2002/07/12 19:28:32 jim Exp $
"""
__metaclass__ = type

from Zope.App.Traversing.IPhysicallyLocatable import IPhysicallyLocatable
from Zope.App.Traversing.IContainmentRoot import IContainmentRoot
from Zope.ComponentArchitecture import getAdapter
from Zope.Proxy.ContextWrapper import getInnerWrapperData, getWrapperContainer

class WrapperPhysicallyLocatable:
    __doc__ = IPhysicallyLocatable.__doc__

    __implements__ =  IPhysicallyLocatable

    def __init__(self, context):
        self.context = context

    def getPhysicalRoot(self):
        "See Zope.App.Traversing.IPhysicallyLocatable.IPhysicallyLocatable"
        container = getWrapperContainer(self.context)
        if container is None:
            raise TypeError("Not enough context to determine location root")
        return getAdapter(container, IPhysicallyLocatable).getPhysicalRoot()

    def getPhysicalPath(self):
        "See Zope.App.Traversing.IPhysicallyLocatable.IPhysicallyLocatable"
        context = self.context
        container = getWrapperContainer(context)
        if container is None:
            raise TypeError("Not enough context to determine location")
        name = getInnerWrapperData(context)['name']

        container = getAdapter(container, IPhysicallyLocatable)
        container_path = container.getPhysicalPath()

        if name == '.':
            # skip
            return container_path

        return container_path + (name, )
        

class RootPhysicallyLocatable:
    __doc__ = IPhysicallyLocatable.__doc__

    __implements__ =  IPhysicallyLocatable

    __used_for__ = IContainmentRoot

    def __init__(self, context):
        self.context = context

    def getPhysicalPath(self):
        "See Zope.App.Traversing.IPhysicallyLocatable.IPhysicallyLocatable"
        return ('', )

    def getPhysicalRoot(self):
        "See Zope.App.Traversing.IPhysicallyLocatable.IPhysicallyLocatable"
        return self.context



