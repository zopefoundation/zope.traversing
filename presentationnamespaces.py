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

$Id: presentationnamespaces.py,v 1.2 2002/12/25 14:13:26 jim Exp $
"""

from zope.component import getView
from zope.app.traversing.namespaces import provideNamespaceHandler
from zope.app.traversing.exceptions import UnexpectedParameters
from zope.exceptions import NotFoundError
from zope.proxy.context import ContextWrapper
from zope.app.traversing.getresource import queryResource

class NoRequest(NotFoundError):
    """Atempt to access a presentation component outside of a request context
    """

def view(name, parameters, pname, ob, request):
    if parameters:
        raise UnexpectedParameters(parameters)
    if not request:
        raise NoRequest(pname)
    return getView(ob, name, request)

def resource(name, parameters, pname, ob, request):
    if parameters:
        raise UnexpectedParameters(parameters)
    if not request:
        raise NoRequest(pname)

    resource = queryResource(ob, name, request)
    if resource is None:
        raise NotFoundError(ob, pname)

    return resource
