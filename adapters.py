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
$Id: adapters.py,v 1.12 2003/06/20 06:53:56 stevea Exp $
"""

from zope.exceptions import NotFoundError

from zope.app.interfaces.traversing import IPhysicallyLocatable
from zope.app.interfaces.traversing import IContainmentRoot
from zope.app.interfaces.traversing import ITraverser, ITraversable

from zope.component import getAdapter, queryAdapter
from zope.context import getInnerWrapperData, getWrapperContainer
from zope.app.context import ContextWrapper

from zope.app.traversing.namespace import namespaceLookup
from zope.app.traversing.namespace import UnexpectedParameters
from zope.app.traversing.namespace import parameterizedNameParse

from zope.interface import implements

from types import StringTypes, MethodType

__metaclass__ = type
_marker = object()  # opaque marker that doesn't get security proxied

class DefaultTraversable:
    """Traverses objects via attribute and item lookup"""

    implements(ITraversable)

    def __init__(self, subject):
        self._subject = subject

    def traverse(self, name, parameters, pname, furtherPath):
        if parameters:
            raise UnexpectedParameters(parameters)
        subject = self._subject
        r = getattr(subject, name, _marker)
        if r is not _marker:
            # XXX It is pretty obvious that we should call methods.
            #     That much is expected from page templates.
            #     What about classmethods / staticmethods / other descriptors?
            #     What about methods that take several arguments?
            if r.__class__ == MethodType:
                return r()
            return r

        if hasattr(subject, '__getitem__'):
            # Let exceptions propagate.
            return subject[name]
        else:
            raise NotFoundError(subject, name)

class WrapperPhysicallyLocatable:
    __doc__ = IPhysicallyLocatable.__doc__

    implements(IPhysicallyLocatable)

    def __init__(self, context):
        self.context = context

    def getRoot(self):
        "See IPhysicallyLocatable"
        container = getWrapperContainer(self.context)
        if container is None:
            raise TypeError("Not enough context to determine location root")
        return getAdapter(container, IPhysicallyLocatable).getRoot()

    def getPath(self):
        "See IPhysicallyLocatable"
        context = self.context
        container = getWrapperContainer(context)
        if container is None:
            raise TypeError("Not enough context to determine location")
        name = getInnerWrapperData(context)['name']

        container = getAdapter(container, IPhysicallyLocatable)
        container_path = container.getPath()

        if name == '.':
            # skip
            return container_path

        if container_path == u'/':
            return u'/' + name
        else:
            return container_path + u'/' + name

    def getName(self):
        "See IPhysicallyLocatable"
        return getInnerWrapperData(self.context)['name']

class RootPhysicallyLocatable:
    __doc__ = IPhysicallyLocatable.__doc__

    implements(IPhysicallyLocatable)

    __used_for__ = IContainmentRoot

    def __init__(self, context):
        self.context = context

    def getPath(self):
        "See IPhysicallyLocatable"
        return u'/'

    def getRoot(self):
        "See IPhysicallyLocatable"
        return self.context

    def getName(self):
        "See IPhysicallyLocatable"
        return u''

class Traverser:
    """Provide traverse features"""

    implements(ITraverser)

    # This adapter can be used for any object.

    def __init__(self, wrapper):
        self.context = wrapper

    def traverse(self, path, default=_marker, request=None):
        if not path:
            return self.context

        if isinstance(path, StringTypes):
            path = path.split('/')
            if len(path) > 1 and not path[-1]:
                # Remove trailing slash
                path.pop()
        else:
            path = list(path)

        path.reverse()
        pop = path.pop

        curr = self.context
        if not path[-1]:
            # Start at the root
            pop()
            curr = getAdapter(self.context, IPhysicallyLocatable
                              ).getRoot()
        try:
            while path:
                name = pop()
                curr = traversePathElement(curr, name, path, request=request)

            return curr
        except NotFoundError:
            if default == _marker:
                raise
            return default


def traversePathElement(obj, name, further_path, default=_marker,
                        traversable=None, request=None):
    """Traverse a single step 'name' relative to the given object.

    'name' must be a string. '.' and '..' are treated specially, as well as
    names starting with '@' or '+'. Otherwise 'name' will be treated as a
    single path segment.

    'further_path' is a list of names still to be traversed.  This method
    is allowed to change the contents of 'further_path'.

    You can explicitly pass in an ITraversable as the 'traversable'
    argument. If you do not, the given object will be adapted to ITraversable.

    'request' is passed in when traversing from presentation code. This
    allows paths like @@foo to work.

    Raises NotFoundError if path cannot be found and 'default' was not provided.
    """

    if name == '.':
        return obj

    if name == '..':
        # XXX This doesn't look right. Why fall back to obj?
        obj = getWrapperContainer(obj) or obj
        return obj

    if name and name[:1] in '@+':
        ns, nm, parms = parameterizedNameParse(name)
        if ns:
            return namespaceLookup(name, ns, nm, parms, obj, request)
    else:
        parms = ()
        nm = name

    if traversable is None:
        if obj.__class__ == dict:
            # Special-case dicts
            return obj[name]

        traversable = queryAdapter(obj, ITraversable, None)
        if traversable is None:
            raise NotFoundError('No traversable adapter found', obj)

    try:
        next_item = traversable.traverse(nm, parms, name, further_path)
        obj = ContextWrapper(next_item, obj, name=name)
    except NotFoundError:
        if default != _marker:
            return default
        else:
            raise

    return obj
