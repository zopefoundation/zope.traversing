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
from zope.proxy.context import getWrapperContainer, isWrapper

__all__ = ['traverse', 'traverseName', 'objectName', 'getParent',
           'getParents', 'getPath', 'getRoot', 'canonicalPath']

_marker = object()

def joinPath(path, *args):
    """Concatenate a path and various args with slashes"""
    for arg in args:
        path = path.endswith('/') and '%s%s' % (path, arg) \
               or '%s/%s' % (path, arg)
    return path

def getPath(obj):
    """Returns a string representing the physical path to the object.
    """
    return getAdapter(obj, IPhysicallyLocatable).getPath()

def getRoot(obj):
    """Returns the root of the traversal for the given object.
    """
    return getAdapter(obj, IPhysicallyLocatable).getRoot()

def traverse(object, path, default=_marker, request=None):
    """Traverse 'path' relative to the given object.

    'path' is a string with path segments separated by '/'.

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
    traverser = getAdapter(object, ITraverser)
    if default is _marker:
        return traverser.traverse(path, request=request)
    else:
        return traverser.traverse(path, default=default, request=request)

def traverseName(obj, name, default=_marker, traversable=None, request=None):
    """Traverse a single step 'name' relative to the given object.

    'name' must be a string. '.' and '..' are treated specially, as well as
    names starting with '@' or '+'. Otherwise 'name' will be treated as a
    single path segment.

    You can explicitly pass in an ITraversable as the 'traversable'
    argument. If you do not, the given object will be adapted to ITraversable.

    'request' is passed in when traversing from presentation code. This
    allows paths like @@foo to work.

    Raises NotFoundError if path cannot be found and 'default' was not provided.
    """
    further_path = []
    if default is _marker:
        obj = traversePathElement(obj, name, further_path,
                                  traversable=traversable, request=request)
    else:
        obj = traversePathElement(obj, name, further_path, default=default,
                                  traversable=traversable, request=request)
    if further_path:
        raise NotImplementedError('further_path returned from traverse')
    else:
        return obj

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
        parent = getWrapperContainer(obj)
        if parent is not None:
            return parent
    raise TypeError("Not enough context information to get parent", obj)

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

def canonicalPath(path_or_object):
    """Returns a canonical absolute unicode path for the given path or object.

    Resolves segments that are '.' or '..'.

    Raises ValueError if a badly formed path is given.
    """
    if isinstance(path_or_object, (str, unicode)):
        path = path_or_object
        if not path:
            raise ValueError("path must be non-empty: %s" % path)
    else:
        path = getPath(path_or_object)

    path = unicode(path)

    # Special case for the root path.
    if path == u'/':
        return path

    if path[0] != u'/':
        raise ValueError('canonical path must start with a "/": %s' % path)
    if path[-1] == u'/':
        raise ValueError('path must not end with a "/": %s' % path)

    # Break path into segments. Process '.' and '..' segments.
    new_segments = []
    for segment in path.split(u'/')[1:]:  # skip empty segment at the start
        if segment == u'.':
            continue
        if segment == u'..':
            new_segments.pop()  # raises IndexError if there is nothing to pop
            continue
        if not segment:
            raise ValueError('path must not contain empty segments: %s'
                             % path)
        new_segments.append(segment)

    return u'/' + (u'/'.join(new_segments))

# import this down here to avoid circular imports
from zope.app.traversing.adapters import traversePathElement
