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

$Id: Namespaces.py,v 1.4 2002/07/12 19:28:32 jim Exp $
"""

from Zope.Exceptions import NotFoundError
from Zope.Proxy.ContextWrapper import ContextWrapper
from Zope.Configuration.Action import Action

_namespace_handlers = {}

def provideNamespaceHandler(ns, handler):
    _namespace_handlers[ns] = handler

def directive(_context, name, handler):
    handler = _context.resolve(handler)
    return [Action(
               discriminator=("traversalNamespace", name),
               callable=provideNamespaceHandler,
               args=(name, handler),
               )]

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
