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
from zope.app.interfaces.traversing.traversable import ITraversable
from zope.exceptions import NotFoundError
from zope.app.traversing.exceptions import UnexpectedParameters

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
