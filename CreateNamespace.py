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

$Id: CreateNamespace.py,v 1.2 2002/06/10 23:28:17 jim Exp $
"""

from Zope.ComponentArchitecture import getService
from Namespaces import provideNamespaceHandler
from Exceptions import UnexpectedParameters
from Zope.Exceptions import NotFoundError
from Zope.Proxy.ContextWrapper import ContextWrapper

def create(name, parameters, pname, ob, request):
    if parameters:
        raise UnexpectedParameters(parameters)

    for addable in getService(ob, 'AddableContent').getAddables(ob):
        if addable.id == name:
            return ContextWrapper(addable, ob, name=name)
        
    raise NotFoundError(ob, pname)

provideNamespaceHandler('create', create)
