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
from Traverser import WrapperChain as _WrapperChain
from Zope.Proxy.ContextWrapper import getWrapperContext as _getWrapperContext
from Zope.Proxy.ContextWrapper import isWrapper as _isWrapper
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
    if not _isWrapper(place):
        raise TypeError, "Not enough context information to traverse"
    traverser = _getAdapter(place, _ITraverser)
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
    """Returns a tuple of names representing the physical path to the
    given object.
    
    Raises TypeError if the given object is not context wrapped
    """
    if not _isWrapper(obj):
        raise TypeError, "Not enough context information to traverse"
    
    return _getAdapter(obj, _ITraverser).getPhysicalPath()
    
def getPhysicalRoot(obj):
    """Returns the root of the traversal for the given object.
    
    Raises TypeError if the given object is not context wrapped
    """
    if not _isWrapper(obj):
        raise TypeError, "Not enough context information to traverse"
        
    return _getAdapter(obj, _ITraverser).getPhysicalRoot()

