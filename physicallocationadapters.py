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

$Id: physicallocationadapters.py,v 1.3 2002/12/28 14:13:28 stevea Exp $
"""
__metaclass__ = type

from zope.app.interfaces.traversing import IPhysicallyLocatable
from zope.app.interfaces.traversing import IContainmentRoot
from zope.component import getAdapter
from zope.proxy.context import getInnerWrapperData, getWrapperContainer

class WrapperPhysicallyLocatable:
    __doc__ = IPhysicallyLocatable.__doc__

    __implements__ =  IPhysicallyLocatable

    def __init__(self, context):
        self.context = context

    def getPhysicalRoot(self):
        "See IPhysicallyLocatable"
        container = getWrapperContainer(self.context)
        if container is None:
            raise TypeError("Not enough context to determine location root")
        return getAdapter(container, IPhysicallyLocatable).getPhysicalRoot()

    def getPhysicalPath(self):
        "See IPhysicallyLocatable"
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
        "See IPhysicallyLocatable"
        return ('', )

    def getPhysicalRoot(self):
        "See IPhysicallyLocatable"
        return self.context
