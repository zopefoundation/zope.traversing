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
"""Default implementation of ITraverser.

$Id: Traverser.py,v 1.2 2002/06/10 23:28:17 jim Exp $
"""

from ITraverser import ITraverser
from ITraversable import ITraversable
from Zope.ContextWrapper.IWrapper import IWrapper
from Zope.Proxy.ContextWrapper import getWrapperContext, getWrapperData
from Zope.Proxy.ContextWrapper import ContextWrapper
from Zope.ComponentArchitecture import queryAdapter
from Zope.Exceptions import NotFoundError, Unauthorized
from Namespaces import namespaceLookup
from ParameterParsing import parameterizedNameParse
from Zope.Security.SecurityManagement import getSecurityManager

from types import StringTypes

from __future__ import generators

# A chain generator; let's us walk the wrapper chain down to the root
def WrapperChain(w):
    while w is not None:
        yield w
        w = getWrapperContext(w)

_marker = object()

class Traverser:
    """Provide traverse features"""

    __implements__ = ITraverser

    # This adapter can be used for any object.

    def __init__(self, wrapper):
        self._wrapper = wrapper

    def getPhysicalRoot(self):
        # Loop over all wrappers until the last one, which is the root.
        for w in WrapperChain(self._wrapper):
            pass
        return w

    def getPhysicalPath(self):
        path = []
        
        for w in WrapperChain(self._wrapper):
            d = getWrapperData(w)
            if d:
                path.insert(0, d['name'])

        return tuple(path)
    
    def traverse(self, path, default=_marker, request=None):
        if not path:
            return self._wrapper

        if isinstance(path, StringTypes):
            path = path.split('/')
            if len(path) > 1 and not path[-1]:
                # Remove trailing slash
                path.pop()
        else:
            path = list(path)

        path.reverse()
        pop = path.pop

        curr = self._wrapper
        if not path[-1]:
            # Start at the root
            pop()
            curr = self.getPhysicalRoot()
        try:
            while path:
                name = pop()

                if name == '.':
                    continue

                if name == '..':
                    curr = getWrapperContext(curr) or curr
                    continue


                if name and name[:1] in '@+':
                    ns, nm, parms = parameterizedNameParse(name)
                    if ns:
                        curr = namespaceLookup(name, ns, nm, parms,
                                               curr, request)
                        continue
                else:
                    parms = ()
                    nm = name

                traversable = queryAdapter(curr, ITraversable, None)
                if traversable is None:
                    raise NotFoundError, 'No traversable adapter found'

                next = traversable.traverse(nm, parms, name, path)
                curr = ContextWrapper(next, curr, name=name)

            return curr

        except:
            if default == _marker:
                raise
            return default


