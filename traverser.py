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

$Id: traverser.py,v 1.2 2002/12/25 14:13:26 jim Exp $
"""

from zope.component import getAdapter
from zope.proxy.context import getWrapperContainer
from zope.proxy.context import ContextWrapper
from zope.component import queryAdapter
from zope.exceptions import NotFoundError
from zope.app.traversing.namespaces import namespaceLookup
from zope.app.traversing.parameterparsing import parameterizedNameParse

from zope.app.interfaces.traversing.physicallylocatable import IPhysicallyLocatable
from zope.app.interfaces.traversing.traverser import ITraverser
from zope.app.interfaces.traversing.traversable import ITraversable

from types import StringTypes

from __future__ import generators

# A chain generator; let's us walk the wrapper chain down to the root
def WrapperChain(w):
    while w is not None:
        yield w
        w = getWrapperContainer(w)

_marker = object()

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
                              ).getPhysicalRoot()
        try:
            while path:
                name = pop()

                if name == '.':
                    continue

                if name == '..':
                    # XXX This doesn't look right. Why fall back to curr?
                    curr = getWrapperContainer(curr) or curr
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
                    raise NotFoundError(
                        'No traversable adapter found', curr)

                next = traversable.traverse(nm, parms, name, path)
                curr = ContextWrapper(next, curr, name=name)

            return curr
        except NotFoundError:
            if default == _marker:
                raise
            return default
