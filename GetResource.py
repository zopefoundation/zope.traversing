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
"""

$Id: GetResource.py,v 1.1 2002/06/13 23:15:44 jim Exp $
"""

from Zope.ComponentArchitecture import getService
from Zope.Exceptions import NotFoundError
from Zope.Proxy.ContextWrapper import ContextWrapper

def getResource(ob, name, request):
    resource = queryResource(ob, name, request)
    if resource is None:
        raise NotFoundError(ob, name)
    return resource

def queryResource(ob, name, request, default=None):
    resource_service = getService(ob, 'Resources')
    resource = resource_service.queryResource(ob, name, request)
    if resource is None:
        return default
    return ContextWrapper(resource, resource_service, name=name)
    

