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
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id: modulenamespace.py,v 1.2 2002/12/25 14:13:26 jim Exp $
"""

from zope.app.interfaces.services.service import INameResolver
from zope.component import getServiceManager, getAdapter
from zope.component import queryDefaultViewName
from zope.interface import Interface


def module(name, parameters, pname, ob, request):
    """Used to traverse to a module (in dot notation)"""
    servicemanager = getServiceManager(ob)
    adapter = getAdapter(servicemanager, INameResolver)
    if adapter is not None:
        ob = adapter.resolve(name)
    if queryDefaultViewName(ob, request) is None:
        return Interface
    return ob
