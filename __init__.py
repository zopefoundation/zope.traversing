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
Convenience functions for traversing the object tree.
"""
from zope.component import getAdapter
from zope.app.interfaces.traversing import IObjectName, IContainmentRoot
from zope.app.interfaces.traversing import ITraverser, IPhysicallyLocatable
# XXX moved to later on to avoid byzantine circular import
#from zope.app.traversing.adapters import Traverser
from zope.proxy.context import getWrapperContext, isWrapper
from zope.proxy.context import getWrapperContainer
from types import StringTypes

__all__ = ['traverse', 'traverseName', 'objectName', 'getParent',
           'getParents', 'getPhysicalPath', 'getPhysicalPathString',
           'getPhysicalRoot', 'locationAsTuple', 'locationAsUnicode']

_marker = object()

def traverse(place, path, default=_marker, request=None):
    """Traverse 'path' relative to 'place'

    'path' can be a string with path segments separated by '/'
    or a sequence of path segments.

    'request' is passed in when traversing from presentation code. This
    allows paths like @@foo to work.

    Raises NotFoundError if path cannot be found
    Raises TypeError if place is not context wrapped

    Note: calling traverse with a path argument taken from an untrusted
          source, such as an HTTP request form variable, is a bad idea.
          It could allow a maliciously constructed request to call
          code unexpectedly.
          Consider using traverseName instead.
    """
    from zope.app.traversing.adapters import Traverser
    traverser = Traverser(place)
    if default is _marker:
        return traverser.traverse(path, request=request)
    else:
        return traverser.traverse(path, default=default, request=request)

# XXX This should have an additional optional argument where you
#     can pass an ITraversable to use, otherwise it should get
#     an adapter for ITraversable from the object and use that to
#     traverse one step.
def traverseName(obj, name, default=_marker):
    """Traverse a single step 'name' relative to 'place'

    'name' must be a string. 'name' will be treated as a single
    path segment, no matter what characters it contains.

    Raises NotFoundError if path cannot be found
    Raises TypeError if place is not context wrapped
    """
    # by passing [name] to traverse (above), we ensure that name is
    # treated as a single path segment, regardless of any '/' characters
    return traverse(obj, [name], default=default)

def objectName(obj):
    """Get the name an object was traversed via

    Raises TypeError if the object is not context-wrapped
    """
    return getAdapter(obj, IObjectName)()

def getParent(obj):
    """Returns the container the object was traversed via.

    Returns None if the object is a containment root.
    Raises TypeError if the object doesn't have enough context to get the
    parent.
    """
    if IContainmentRoot.isImplementedBy(obj):
        return None
    if isWrapper(obj):
        parent = getWrapperContext(obj)
        if parent is not None:
            return parent
    raise TypeError, "Not enough context information to get parent"

def getParents(obj):
    """Returns a list starting with the given object's parent followed by
    each of its parents.
    
    Raises a TypeError if the context doesn't go all the way down to
    a containment root.
    """
    if IContainmentRoot.isImplementedBy(obj):
        return []
    if isWrapper(obj):
        parents = []
        w = obj
        while 1:
            w = getWrapperContainer(w)
            if w is None:
                break
            parents.append(w)
            
        if parents and IContainmentRoot.isImplementedBy(parents[-1]):
            return parents
    raise TypeError, "Not enough context information to get all parents"

def getPhysicalPath(obj):
    """Returns a tuple of names representing the physical path to the object.
    """
    return getAdapter(obj, IPhysicallyLocatable).getPhysicalPath()

def getPhysicalPathString(obj):
    """Returns a string representing the physical path to the object.
    """
    path = getAdapter(obj, IPhysicallyLocatable).getPhysicalPath()
    return locationAsUnicode(path)

def getPhysicalRoot(obj):
    """Returns the root of the traversal for the given object.
    """
    return getAdapter(obj, IPhysicallyLocatable).getPhysicalRoot()

def locationAsTuple(location):
    """Given a location as a unicode or ascii string or as a tuple of
    unicode or ascii strings, returns the location as a tuple of
    unicode strings.

    Raises a ValueError if a poorly formed location is given.
    """
    if not location:
        raise ValueError("location must be non-empty: %s" % repr(location))
    if isinstance(location, StringTypes):
        if location == u'/':  # matches '/' or u'/'
            return (u'',)
        t = tuple(location.split(u'/'))
    elif location.__class__ == tuple:
        # isinstance doesn't work when tuple is security-wrapped
        t = tuple(map(unicode, location))
    else:
        raise ValueError("location must be a string or a tuple of strings: %s"
                         % repr(location))

    if len(t) > 1 and t[-1] == u'':  # matches '' or u''
        raise ValueError("location tuple must not end with empty string: %s"
                         % repr(t))
    if '' in t[1:]:
        raise ValueError("location tuple must not contain '' except at the"
                         " start: %s" % repr(t))
    return t

def locationAsUnicode(location):
    """Given a location as a unicode or ascii string or as a tuple of
    unicode or ascii strings, returns the location as a slash-separated
    unicode string.

    Raises ValueError if a poorly formed location is given.
    """
    if not location:
        raise ValueError("location must be non-empty: %s" % repr(location))
    if isinstance(location, StringTypes):
        u = unicode(location)
    elif location.__class__ == tuple:
        # isinstance doesn't work when tuple is security-wrapped
        u = u'/'.join(location)
        if not u:  # special case for u''
            return u'/'
    else:
        raise ValueError("location must be a string or a tuple of strings: %s"
                         % repr(location))
    if u != '/' and u[-1] == u'/':
        raise ValueError("location must not end with a slash: %s" % u)
    if u.find(u'//') != -1:
        raise ValueError("location must not contain // : %s" % u)
    return u

