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

$Id: SkinNamespace.py,v 1.3 2002/12/20 19:45:45 jim Exp $
"""

from Namespaces import provideNamespaceHandler
from Exceptions import UnexpectedParameters
from Zope.Exceptions import NotFoundError

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
