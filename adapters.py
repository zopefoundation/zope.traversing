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
$Id: adapters.py,v 1.5 2003/03/24 16:42:22 mgedmin Exp $
"""

from zope.exceptions import NotFoundError

from zope.app.interfaces.traversing import IObjectName, IPhysicallyLocatable
from zope.app.interfaces.traversing import IContainmentRoot
from zope.app.interfaces.traversing import ITraverser, ITraversable

from zope.component import getAdapter, queryAdapter
from zope.proxy.context import getInnerWrapperData, getWrapperContainer
from zope.proxy.context import ContextWrapper

from zope.app.traversing.namespace import namespaceLookup
from zope.app.traversing.namespace import UnexpectedParameters
from zope.app.traversing.namespace import parameterizedNameParse

from types import StringTypes

__metaclass__ = type
_marker = object()  # opaque marker that doesn't get security proxied

class DefaultTraversable:
    """Traverses objects via attribute and item lookup"""

    __implements__ = ITraversable

    def __init__(self, subject):
        self._subject = subject

    def traverse(self, name, parameters, pname, furtherPath):
        if parameters:
            raise UnexpectedParameters(parameters)
        subject = self._subject
        r = getattr(subject, name, _marker)
        if r is not _marker:
            return r

        if hasattr(subject, '__getitem__'):
            # Let exceptions propagate.
            return self._subject[name]
        else:
            raise NotFoundError(self._subject, name)

class ObjectName(object):

    __implements__ = IObjectName

    def __init__(self, context):
        self.context = context

    def __str__(self):
        dict = getInnerWrapperData(self.context)
        name = dict and dict.get('name') or None
        if name is None:
            raise TypeError, \
                  'Not enough context information to get an object name'
        return name

    __call__ = __str__


class SiteObjectName(object):

    __implements__ = IObjectName

    def __init__(self, context):
        pass

    def __str__(self):
        return ''

    __call__ = __str__

class WrapperPhysicallyLocatable:
    __doc__ = IPhysicallyLocatable.__doc__

    __implements__ =  IPhysicallyLocatable

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

class RootPhysicallyLocatable:
    __doc__ = IPhysicallyLocatable.__doc__

    __implements__ =  IPhysicallyLocatable

    __used_for__ = IContainmentRoot

    def __init__(self, context):
        self.context = context

    def getPath(self):
        "See IPhysicallyLocatable"
        return u'/'

    def getRoot(self):
        "See IPhysicallyLocatable"
        return self.context

class Traverser:
    """Provide traverse features"""

    __implements__ = ITraverser

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
