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

$Id: namespace.py,v 1.1 2002/12/28 17:49:33 stevea Exp $
"""

from zope.interface import Interface
from zope.exceptions import NotFoundError
from zope.proxy.context import ContextWrapper, getWrapperObject
from zope.proxy.context import getWrapperContext
from zope.configuration.action import Action
from zope.component import queryAdapter, getAdapter, getServiceManager
from zope.component import queryDefaultViewName, getView, getService

from zope.app.interfaces.traversing import ITraversable
from zope.app.applicationcontrol.applicationcontrol \
    import applicationController
from zope.app.content.folder import RootFolder
from zope.app.interfaces.services.service import INameResolver

import re

class UnexpectedParameters(NotFoundError):
    "Unexpected namespace parameters were provided."

class ExcessiveWrapping(NotFoundError):
    "Too many levels of acquisition wrapping. We don't believe them."

class NoRequest(NotFoundError):
    "Attempt to access a presentation component outside of a request context."


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


namespace_pattern = re.compile('[+][+]([a-zA-Z0-9_]+)[+][+]')

def parameterizedNameParse(name):
    """Parse a name with parameters, including namespace parameters.

    Return:

    - namespace, or None if there isn't one.

    - unparameterized name.

    - sequence of parameters, as name-value pairs.
    """

    ns = ''
    if name.startswith('@@'):
        ns = 'view'
        name = name[2:]
    else:
        match = namespace_pattern.match(name)
        if match:
            prefix, ns = match.group(0, 1)
            name = name[len(prefix):]

    return ns, name, ()

def getResourceInContext(ob, name, request):
    resource = queryResourceInContext(ob, name, request)
    if resource is None:
        raise NotFoundError(ob, name)
    return resource

def queryResourceInContext(ob, name, request, default=None):
    resource_service = getService(ob, 'Resources')
    resource = resource_service.queryResource(ob, name, request)
    if resource is None:
        return default
    return ContextWrapper(resource, resource_service, name=name)


# ---- namespace processors below ----

def acquire(name, parameters, pname, ob, request):
    if parameters:
        raise UnexpectedParameters(parameters)

    i = 0
    origOb = ob
    while i < 200:
        i += 1
        traversable = queryAdapter(ob, ITraversable, None)
        if traversable is not None:

            try:
                # XXX what do we do if the path gets bigger?
                path = []
                next = traversable.traverse(name, parameters, pname, path)
                if path: continue
            except NotFoundError:
                pass
            else:
                return ContextWrapper(next, ob, name=name)

        ob = getWrapperContext(ob)
        if ob is None:
            raise NotFoundError(origOb, pname)

    raise ExcessiveWrapping(origOb, pname)

def attr(name, parameters, pname, ob, request):
    if parameters:
        raise UnexpectedParameters(parameters)
    return getattr(ob, name)

def item(name, parameters, pname, ob, request):
    if parameters:
        raise UnexpectedParameters(parameters)
    return ob[name]

def etc(name, parameters, pname, ob, request):
    # XXX

    # This is here now to allow us to get service managers from a
    # separate namespace from the content. We add and etc
    # namespace to allow us to handle misc objects.  We'll apply
    # YAGNI for now and hard code this. We'll want something more
    # general later. We were thinking of just calling "get"
    # methods, but this is probably too magic. In particular, we
    # will treat returned objects as sub-objects wrt security and
    # not all get methods may satisfy this assumption. It might be
    # best to introduce some sort of etc registry.

    if parameters:
        raise UnexpectedParameters(parameters)

    if name == 'ApplicationController' and ob.__class__ == RootFolder:
        return applicationController

    if name != 'Services':

        raise NotFoundError(ob, pname, request)

    method_name = "getServiceManager"
    method = getattr(ob, method_name, None)
    if method is None:
        raise NotFoundError(ob, pname, request)

    return method()

def module(name, parameters, pname, ob, request):
    """Used to traverse to a module (in dot notation)"""
    servicemanager = getServiceManager(ob)
    adapter = getAdapter(servicemanager, INameResolver)
    if adapter is not None:
        ob = adapter.resolve(name)
    if queryDefaultViewName(ob, request) is None:
        return Interface
    return ob

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

    resource = queryResourceInContext(ob, name, request)
    if resource is None:
        raise NotFoundError(ob, pname)

    return resource

def skin(name, parameters, pname, ob, request):

    if parameters:
        raise UnexpectedParameters(parameters)

    if not request:
        raise NoRequest(pname)

    request.setViewSkin(name)

    return ob
