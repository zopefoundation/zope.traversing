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

$Id: Namespaces.py,v 1.5 2002/07/13 14:18:36 jim Exp $
"""

from Zope.Exceptions import NotFoundError
from Zope.Proxy.ContextWrapper import ContextWrapper, getWrapperObject
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

    The resulting object is returned in the context of the original.
    This means that the caller should *not* wrap the result.
    """
    
    handler = _namespace_handlers.get(ns)
    if handler is None:
        raise NotFoundError(name)

    new = handler(qname, parameters, name, object, request)
    if new is object:    
        # The handler had a side effect only and didn't look up a
        # different object.  We want to retain the side-effect name
        # for things like URLs.

        # But wait, there's more. The object may be wrapped. If the
        # object is already wrapped and we return the object in the
        # context of itself, the containment context will be wrong,
        # because the inner wrapper will be the original object, so
        # our added layer with the name we want to preserve will be
        # ignored when searching containment.
        
        # For this reason, we'll remove a layer of wrapping from new
        # before we put it in context.

        new = getWrapperObject(new)
        
        new = ContextWrapper(new, object, name='.', side_effect_name=name)

    else:
        new = ContextWrapper(new, object, name=name)

    return new
