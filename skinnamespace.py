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

$Id: skinnamespace.py,v 1.2 2002/12/25 14:13:26 jim Exp $
"""

from zope.app.traversing.namespaces import provideNamespaceHandler
from zope.app.traversing.exceptions import UnexpectedParameters
from zope.exceptions import NotFoundError

class NoRequest(NotFoundError):
    """Atempt to access a presentation component outside of a request context
    """

def skin(name, parameters, pname, ob, request):

    if parameters:
        raise UnexpectedParameters(parameters)

    if not request:
        raise NoRequest(pname)

    request.setViewSkin(name)

    return ob
