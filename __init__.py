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
Traversing the object tree.
"""
# being careful not to pollute the namespace unnecessarily...
from Zope.ComponentArchitecture import getAdapter as _getAdapter
from ObjectName import IObjectName as _IObjectName
from ITraverser import ITraverser as _ITraverser
from IPhysicallyLocatable import IPhysicallyLocatable as _IPhysicallyLocatable
from Traverser import WrapperChain as _WrapperChain
from Traverser import Traverser as _Traverser
from Zope.Proxy.ContextWrapper import getWrapperContext as _getWrapperContext
from Zope.Proxy.ContextWrapper import isWrapper as _isWrapper
from types import StringTypes
_marker = object()

# XXX: this probably shouldn't have "request" in its signature, nor
#      in the arguments of the call to traverser.traverse
def traverse(place, path, default=_marker, request=None):
    """Traverse 'path' relative to 'place'
    
    'path' can be a string with path segments separated by '/'
    or a sequence of path segments.
    
    Raises NotFoundError if path cannot be found
    Raises TypeError if place is not context wrapped
    
    Note: calling traverse with a path argument taken from an untrusted
          source, such as an HTTP request form variable, is a bad idea.
          It could allow a maliciously constructed request to call 
          code unexpectedly.
          Consider using traverseName instead.
    """
    traverser = _Traverser(place)
    if default is _marker:
        return traverser.traverse(path, request=request)
    else:
        return traverser.traverse(path, default=default, request=request)

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
    return _getAdapter(obj, _IObjectName)()
    
def getParent(obj):
    """Returns the container the object was traversed via.
    
    Raises TypeError if the given object is not context wrapped
    """
    if not _isWrapper(obj):
        raise TypeError, "Not enough context information to traverse"
    return _getWrapperContext(obj)
    
def getParents(obj):
    """Returns a list starting with the given object's parent followed by
    each of its parents.
    
    Raises TypeError if the given object is not context wrapped
    """
    if not _isWrapper(obj):
        raise TypeError, "Not enough context information to traverse"
    iterator = _WrapperChain(obj)
    iterator.next()  # send head of chain (current object) to /dev/null
    return [p for p in iterator]
    
def getPhysicalPath(obj):
    """Returns a tuple of names representing the physical path to the object.
    
    Raises TypeError if the given object is not context wrapped
    """
    return _getAdapter(obj, _IPhysicallyLocatable).getPhysicalPath()

def getPhysicalPathString(obj):
    """Returns a string representing the physical path to the object.
    
    Raises TypeError if the given object is not context wrapped
    """
    path = _getAdapter(obj, _IPhysicallyLocatable).getPhysicalPath()
    return locationAsUnicode(path)
    
    
def getPhysicalRoot(obj):
    """Returns the root of the traversal for the given object.
    
    Raises TypeError if the given object is not context wrapped
    """
    return _getAdapter(obj, _IPhysicallyLocatable).getPhysicalRoot()

def locationAsTuple(location):
    """Given a location as a unicode or ascii string or as a tuple of
    unicode or ascii strings, returns the location as a tuple of
    unicode strings.
    
    Raises a ValueError if a poorly formed location is given.
    """
    if not location:
        raise ValueError, "location must be non-empty: %s" % repr(location)
    if isinstance(location, tuple):
        t = tuple(map(unicode, location))
    elif isinstance(location, StringTypes):
        if location == u'/':  # matches '/' or u'/'
            return (u'',)
        t = tuple(location.split(u'/'))
    else:
        raise ValueError, \
            "location %s must be a string or a tuple of strings." % (location,)
        
    if len(t) > 1 and t[-1] == u'':  # matches '' or u''
        raise ValueError, \
            "location tuple %s must not end with empty string." % (t,)
    # don't usually need this, so just an assertion rather than a value error
    assert '' not in t[1:]
    return t
    
def locationAsUnicode(location):
    """Given a location as a unicode or ascii string or as a tuple of
    unicode or ascii strings, returns the location as a slash-separated
    unicode string.
    
    Raises ValueError if a poorly formed location is given.
    """
    if not location:
        raise ValueError, "location must be non-empty."
    if isinstance(location, tuple):
        u = u'/'.join(location)
        if not u:  # special case for u''
            return u'/'
    elif isinstance(location, StringTypes):
        u = unicode(location)
    else:
        raise ValueError, \
            "location %s must be a string or a tuple of strings." % (location,)
    if u != '/' and u[-1] == u'/':
        raise ValueError, "location %s must not end with a slash." % u
    # don't usually need this, so just an assertion rather than a value error
    assert u.find(u'//') == -1
    return u
