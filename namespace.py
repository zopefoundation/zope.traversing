##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""URL Namespace Implementations

$Id$
"""
import re
import zope.interface
from zope import component
from zope.component.servicenames import Presentation
from zope.exceptions import NotFoundError

from zope.app.traversing.interfaces import ITraversable, IPathAdapter
from zope.security.proxy import removeSecurityProxy

class UnexpectedParameters(NotFoundError):
    "Unexpected namespace parameters were provided."

class ExcessiveWrapping(NotFoundError):
    "Too many levels of acquisition wrapping. We don't believe them."

def namespaceLookup(ns, name, object, request=None):
    """Lookup a value from a namespace

       We look up a value using a view or an adapter, depending on
       whether a request is passed.

       Let's start with adapter-based transersal. We're going to use the
       component architecture, so we'll need to initialize it:

         >>> from zope.app.tests.placelesssetup import setUp, tearDown
         >>> setUp()

         >>> class I(zope.interface.Interface):
         ...     'Test interface'
         >>> class C(object):
         ...     zope.interface.implements(I)

       We'll register a simple testing adapter:

         >>> class Adapter(object):
         ...     def __init__(self, context):
         ...         self.context = context
         ...     def traverse(self, name, remaining):
         ...         return name+'42'

         >>> from zope.app.tests import ztapi
         >>> ztapi.provideAdapter(I, ITraversable, Adapter, 'foo')

       Then given an object, we can traverse it with a
       namespace-qualified name:

         >>> namespaceLookup('foo', 'bar', C())
         'bar42'

       If we give an invalid namespace, we'll get a not found error:

         >>> namespaceLookup('fiz', 'bar', C())
         Traceback (most recent call last):
         ...
         NotFoundError: '++fiz++bar'

       We'll get the same thing if we provide a request:

         >>> from zope.publisher.browser import TestRequest
         >>> request = TestRequest()
         >>> namespaceLookup('foo', 'bar', C(), request)
         Traceback (most recent call last):
         ...
         NotFoundError: '++foo++bar'

       We need to provide a view:

         >>> class View(object):
         ...     def __init__(self, context, request):
         ...         pass
         ...     def traverse(self, name, remaining):
         ...         return name+'fromview'
         >>> ztapi.browserView(I, 'foo', View, providing=ITraversable)

         >>> namespaceLookup('foo', 'bar', C(), request)
         'barfromview'

         >>> tearDown()
       """

    if request is not None:
        traverser = component.queryView(object, ns, request,
                                        providing=ITraversable)
    else:
        traverser = component.queryAdapter(object, ITraversable, ns)

    if traverser is None:
        raise NotFoundError("++%s++%s" % (ns, name))

    return traverser.traverse(name, ())


namespace_pattern = re.compile('[+][+]([a-zA-Z0-9_]+)[+][+]')

def nsParse(name):
    """Parse a namespace-qualified name into a namespace name and a name

    Returns the namespace name and a name.

    A namespace-qualified name is usually of the form ++ns++name, as in:

    >>> nsParse('++acquire++foo')
    ('acquire', 'foo')

    The part inside the +s must be an identifier, so:

    >>> nsParse('++hello world++foo')
    ('', '++hello world++foo')
    >>> nsParse('+++acquire+++foo')
    ('', '+++acquire+++foo')


    But it may also be a @@foo, which implies the view namespace:

    >>> nsParse('@@foo')
    ('view', 'foo')

    >>> nsParse('@@@foo')
    ('view', '@foo')

    >>> nsParse('@foo')
    ('', '@foo')

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

    return ns, name

def getResource(site, name, request):
    resource = queryResource(site, name, request)
    if resource is None:
        raise NotFoundError(site, name)
    return resource

def queryResource(site, name, request, default=None):
    resource = component.queryResource(name, request)
    if resource is None:
        return default

    # We need to set the __parent__ and __name__.  We need the unproxied
    # resource to do this.  We still return the proxied resource.
    r = removeSecurityProxy(resource)

    r.__parent__ = site
    r.__name__ = name

    return resource

# ---- namespace processors below ----

class SimpleHandler(object):

    zope.interface.implements(ITraversable)

    def __init__(self, context, request=None):
        """Simple handlers can be used as adapters or views

           They ignore their second constructor arg and store the first
           one in their context attr:

              >>> SimpleHandler(42).context
              42

              >>> SimpleHandler(42, 43).context
              42
           """
        self.context = context

class acquire(SimpleHandler):
    """Traversal adapter for the acquire namespace
    """

    def traverse(self, name, remaining):
        """Acquire a name

           Let's set up some example data:

             >>> class testcontent(object):
             ...     zope.interface.implements(ITraversable)
             ...     def traverse(self, name, remaining):
             ...         v = getattr(self, name, None)
             ...         if v is None:
             ...             raise NotFoundError(name)
             ...         return v
             ...     def __repr__(self):
             ...         return 'splat'

             >>> ob = testcontent()
             >>> ob.a = 1
             >>> ob.__parent__ = testcontent()
             >>> ob.__parent__.b = 2
             >>> ob.__parent__.__parent__ = testcontent()
             >>> ob.__parent__.__parent__.c = 3

           And acquire some names:

             >>> adapter = acquire(ob)

             >>> adapter.traverse('a', ())
             1

             >>> adapter.traverse('b', ())
             2

             >>> adapter.traverse('c', ())
             3

             >>> adapter.traverse('d', ())
             Traceback (most recent call last):
             ...
             NotFoundError: (splat, 'd')
           """
        i = 0
        ob = self.context
        while i < 200:
            i += 1
            traversable = ITraversable(ob, None)
            if traversable is not None:
                try:
                    # XXX what do we do if the path gets bigger?
                    path = []
                    next = traversable.traverse(name, path)
                    if path:
                        continue
                except NotFoundError:
                    pass
                else:
                    return next

            ob = getattr(ob, '__parent__', None)
            if ob is None:
                raise NotFoundError(self.context, name)

        raise ExcessiveWrapping(self.context, name)

class attr(SimpleHandler):

    def traverse(self, name, ignored):
        """Attribute traversal adapter

           This adapter just provides traversal to attributes:

              >>> ob = {'x': 1}
              >>> adapter = attr(ob)
              >>> adapter.traverse('keys', ())()
              ['x']

           """
        return getattr(self.context, name)

class item(SimpleHandler):

    def traverse(self, name, ignored):
        """Item traversal adapter

           This adapter just provides traversal to items:

              >>> ob = {'x': 42}
              >>> adapter = item(ob)
              >>> adapter.traverse('x', ())
              42
           """
        return self.context[name]

from zope.app.applicationcontrol.applicationcontrol \
     import applicationController
from zope.app.traversing.interfaces import IContainmentRoot

class etc(SimpleHandler):

    def traverse(self, name, ignored):
        # TODO:
        # This is here now to allow us to get service managers from a
        # separate namespace from the content. We add and etc
        # namespace to allow us to handle misc objects.  We'll apply
        # YAGNI for now and hard code this. We'll want something more
        # general later. We were thinking of just calling "get"
        # methods, but this is probably too magic. In particular, we
        # will treat returned objects as sub-objects wrt security and
        # not all get methods may satisfy this assumption. It might be
        # best to introduce some sort of etc registry.

        ob = self.context

        if (name in ('process', 'ApplicationController')
            and IContainmentRoot.providedBy(ob)):
            return applicationController

        if name not in ('site', 'Services'):
            raise NotFoundError(ob, name)

        method_name = "getSiteManager"
        method = getattr(ob, method_name, None)
        if method is None:
            raise NotFoundError(ob, name)

        return method()

class view(object):

    zope.interface.implements(ITraversable)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, ignored):
        view = component.queryView(self.context, name, self.request)
        if view is None:
            raise NotFoundError(self.context, name)

        return view

class resource(view):

    def traverse(self, name, ignored):
        # The context is important here, since it becomes the parent of the
        # resource, which is needed to generate the absolute URL.
        return getResource(self.context, name, self.request)

class skin(view):

    def traverse(self, name, ignored):
        self.request.shiftNameToApplication()
        self.request.setPresentationSkin(name)

        return self.context

class vh(view):

    def traverse(self, name, ignored):

        request = self.request

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
            raise ValueError(
                "Must have a path element '++' after a virtual host "
                "directive.")

        request.setVirtualHostRoot(app_names)

        return self.context


class adapter(SimpleHandler):

    def traverse(self, name, ignored):
        """Adapter traversal adapter

           This adapter provides traversal to named adapters registered to
           provide IPathAdapter.

           To demonstrate this, we need to register some adapters:

             >>> from zope.app.tests.placelesssetup import setUp, tearDown
             >>> setUp()
             >>> from zope.app.tests import ztapi
             >>> def adapter1(ob):
             ...     return 1
             >>> def adapter2(ob):
             ...     return 2
             >>> ztapi.provideAdapter(None, IPathAdapter, adapter1, 'a1')
             >>> ztapi.provideAdapter(None, IPathAdapter, adapter2, 'a2')

           Now, with these adapters in place, we can use the traversal adapter:

             >>> ob = object()
             >>> adapter = adapter(ob)
             >>> adapter.traverse('a1', ())
             1
             >>> adapter.traverse('a2', ())
             2
             >>> try:
             ...     adapter.traverse('bob', ())
             ... except NotFoundError:
             ...     print 'no adapter'
             no adapter

           Cleanup:
    
             >>> tearDown()
           """
        try:
            return component.getAdapter(self.context, IPathAdapter, name)
        except:
            raise NotFoundError(self.context, name)
