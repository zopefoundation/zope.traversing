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

$Id: PresentationNamespaces.py,v 1.3 2002/06/13 23:15:44 jim Exp $
"""

from Zope.ComponentArchitecture import getView
from Namespaces import provideNamespaceHandler
from Exceptions import UnexpectedParameters
from Zope.Exceptions import NotFoundError
from Zope.Proxy.ContextWrapper import ContextWrapper
from GetResource import queryResource

class NoRequest(NotFoundError):
    """Atempt to access a presentation component outside of a request context
    """

def view(name, parameters, pname, ob, request):
    if parameters:
        raise UnexpectedParameters(parameters)
    if not request:
        raise NoRequest(pname)
    return getView(ob, name, request)

provideNamespaceHandler('view', view)

def resource(name, parameters, pname, ob, request):
    if parameters:
        raise UnexpectedParameters(parameters)
    if not request:
        raise NoRequest(pname)

    resource = queryResource(ob, name, request)
    if resource is None:
        raise NotFoundError(ob, pname)

    return resource

provideNamespaceHandler('resource', resource)

