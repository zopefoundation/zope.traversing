##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
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
"""Adapters for the traversing mechanism

$Id$
"""
from types import StringTypes, MethodType

from zope.exceptions import NotFoundError
from zope.interface import implements

from zope.app.traversing.interfaces import IPhysicallyLocatable
from zope.app.traversing.interfaces import IContainmentRoot
from zope.app.traversing.interfaces import ITraverser, ITraversable

from zope.app.traversing.namespace import namespaceLookup
from zope.app.traversing.namespace import UnexpectedParameters
from zope.app.traversing.namespace import nsParse

_marker = object()  # opaque marker that doesn't get security proxied

class DefaultTraversable(object):
    """Traverses objects via attribute and item lookup"""

    implements(ITraversable)

    def __init__(self, subject):
        self._subject = subject

    def traverse(self, name, furtherPath):
        subject = self._subject
        __traceback_info__ = (subject, name, furtherPath)
        attr = getattr(subject, name, _marker)
        if attr is not _marker:
            return attr

        if hasattr(subject, '__getitem__'):
            # Let exceptions propagate.
            return subject[name]
        else:
            raise NotFoundError(subject, name)

class RootPhysicallyLocatable(object):
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

    def getNearestSite(self):
        "See IPhysicallyLocatable"
        return self


class Traverser(object):
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
            curr = IPhysicallyLocatable(self.context).getRoot()
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
        obj = obj.__parent__
        return obj

    if name and name[:1] in '@+':
        ns, nm = nsParse(name)
        if ns:
            return namespaceLookup(ns, nm, obj, request)
    else:
        parms = ()
        nm = name

    if traversable is None:
        if obj.__class__ == dict:
            # Special-case dicts
            return obj[name]

        traversable = ITraversable(obj, None)
        if traversable is None:
            raise NotFoundError('No traversable adapter found', obj)

    try:
        next_item = traversable.traverse(nm, further_path)
        obj = next_item
    except NotFoundError:
        if default != _marker:
            return default
        else:
            raise

    return obj
