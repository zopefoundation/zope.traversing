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

$Id: ITraverser.py,v 1.4 2002/08/13 17:57:05 gvanrossum Exp $
"""

import Interface

_RAISE_KEYERROR=[]

class ITraverser(Interface.Interface):
    """Provide traverse features"""
    
    def traverse(path, default=_RAISE_KEYERROR):
        """
        Return an object given a path.
        
        Path is either an immutable sequence of strings or a slash ('/')
        delimited string.

        If the first string in the path sequence is an empty string,
        or the path begins with a '/', start at the root. Otherwise the path
        is relative to the current context.

        If the object is not found, return 'default' argument.
        """
