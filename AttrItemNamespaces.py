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

$Id: AttrItemNamespaces.py,v 1.2 2002/06/10 23:28:17 jim Exp $
"""

from Namespaces import provideNamespaceHandler
from Exceptions import UnexpectedParameters

def attr(name, parameters, pname, ob, request):
    if parameters:
        raise UnexpectedParameters(parameters)
    return getattr(ob, name)

provideNamespaceHandler('attribute', attr)

def item(name, parameters, pname, ob, request):
    if parameters:
        raise UnexpectedParameters(parameters)
    return ob[name]

provideNamespaceHandler('item', item)


# YAGNI
# 
# def accessor(name, parameters, ob, request):
#     if parameters:
#         raise UnexpectedParameters(parameters)
# 
#     method = getattr(ob, name, None)
#     if method is None: 
#         raise NotFound(ob, name, request)
# 
#     return method()
# 
# provideNamespaceHandler('accessor', accessor)
