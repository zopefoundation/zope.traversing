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

$Id: ModuleNamespace.py,v 1.2 2002/12/19 18:14:03 poster Exp $
"""

from Zope.App.OFS.Services.ServiceManager.INameResolver import INameResolver
from Zope.ComponentArchitecture import getServiceManager, getAdapter
from Zope.ComponentArchitecture import queryDefaultViewName
from Interface import Interface


def module(name, parameters, pname, ob, request):
    """Used to traverse to a module (in dot notation)"""   
    servicemanager = getServiceManager(ob)
    adapter = getAdapter(servicemanager, INameResolver)
    if adapter is not None:
        ob = adapter.resolve(name)
    if queryDefaultViewName(ob, request) is None:
        return Interface
    return ob
