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

$Id: Namespaces.py,v 1.3 2002/06/23 17:03:44 jim Exp $
"""

from Zope.Exceptions import NotFoundError
from Zope.Proxy.ContextWrapper import ContextWrapper

_namespace_handlers = {}

def provideNamespaceHandler(ns, handler):
    _namespace_handlers[ns] = handler

def namespaceLookup(name, ns, qname, parameters, object, request=None):
    """Lookup a value from a namespace

    name -- the original name
    ns -- The namespace
    qname -- The name without any parameters
    """
    
    handler = _namespace_handlers.get(ns)
    if handler is None:
        raise NotFoundError(name)
    new = ContextWrapper(handler(qname, parameters, name, object, request),
                         object, name=name)
    return new

# XXX should get this from zcml
# Register the etc, view, and resource namespaces
import EtcNamespace, PresentationNamespaces, AttrItemNamespaces
import AcquireNamespace
