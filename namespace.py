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
"""URL Namespace Implementations

$Id: namespace.py,v 1.25 2004/03/05 22:09:19 jim Exp $
"""
import re
from zope.app import zapi
from zope.exceptions import NotFoundError
from zope.app.interfaces.traversing import ITraversable
from zope.proxy import removeAllProxies

class UnexpectedParameters(NotFoundError):
    "Unexpected namespace parameters were provided."

class ExcessiveWrapping(NotFoundError):
    "Too many levels of acquisition wrapping. We don't believe them."

class NoRequest(NotFoundError):
    "Attempt to access a presentation component outside of a request context."


_namespace_handlers = {}

def provideNamespaceHandler(ns, handler):
    _namespace_handlers[ns] = handler

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
    resource_service = zapi.getService(ob, zapi.servicenames.Presentation)
    resource = resource_service.queryResource(name, request)
    if resource is None:
        return default

    # We need to set the __parent__ and __name__. We need the unproxied
    # resource to do this.  we will still return the proxied resource.
    r = removeAllProxies(resource)

    r.__parent__ = ob
    r.__name__ = name

    return resource


# ---- namespace processors below ----

def acquire(name, parameters, pname, ob, request):
    if parameters:
        raise UnexpectedParameters(parameters)

    i = 0
    origOb = ob
    while i < 200:
        i += 1
        traversable = zapi.queryAdapter(ob, ITraversable, None)
        if traversable is not None:

            try:
                # XXX what do we do if the path gets bigger?
                path = []
                next = traversable.traverse(name, parameters, pname, path)
                if path:
                    continue
            except NotFoundError:
                pass
            else:
                return next

        ob = getattr(ob, '__parent__', None)
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

from zope.app.applicationcontrol.applicationcontrol \
    import applicationController
from zope.app.interfaces.traversing import IContainmentRoot
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

    if (name in ('process', 'ApplicationController')
        and IContainmentRoot.providedBy(ob)):
        return applicationController

    if name not in ('site', 'Services'):
        raise NotFoundError(ob, pname, request)

    method_name = "getSiteManager"
    method = getattr(ob, method_name, None)
    if method is None:
        raise NotFoundError(ob, pname, request)

    return method()

def help(name, parameters, pname, ob, request):
    """Used to traverse to an online help topic."""
    return zapi.getService(ob, 'OnlineHelp')

def view(name, parameters, pname, ob, request):
    if parameters:
        raise UnexpectedParameters(parameters)
    if not request:
        raise NoRequest(pname)
    view = zapi.queryView(ob, name, request)
    if view is None:
        raise NotFoundError(ob, name)

    return view

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

    request.shiftNameToApplication()
    request.setPresentationSkin(name)

    return ob

def vh(name, parameters, pname, ob, request):

    traversal_stack = request.getTraversalStack()
    app_names = []

    if name:
        try:
            proto, host, port = name.split(":")
        except ValueError:
            raise ValueError("Vhost directive should have the form "
                             "++vh++protocol:host:port")

        request.setApplicationServer(host, proto, port)

    if '++' in traversal_stack:
        segment = traversal_stack.pop()
        while segment != '++':
            app_names.append(segment)
            segment = traversal_stack.pop()
        request.setTraversalStack(traversal_stack)
    else:
        raise ValueError("Must have a path element '++' after a virtual host "
                         "directive.")

    request.setVirtualHostRoot(app_names)
    return ob
