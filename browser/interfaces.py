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
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""Browser traversal interfaces

$Id: interfaces.py,v 1.3 2004/04/27 10:53:50 jim Exp $
"""
from zope.interface import Interface

class IAbsoluteURL(Interface):

    def __str__():
        """Get a human-readable string representation
        """

    def __repr__():
        """Get a string representation
        """

    def __call__():
        """Get a string representation
        """

    def breadcrumbs():
        """Return a tuple like ({'name':name, 'url':url}, ...)

        Name is the name to display for that segment of the breadcrumbs.
        URL is the link for that segment of the breadcrumbs.
        """

class IAbsoluteURLAPI(Interface):

    def absoluteURL(ob, request):
        """Compute the absolute URL of an object
        """
