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
import Interface

class ITraversable(Interface.Interface):
    """To traverse an object, this interface must be provided"""

    def traverse(name, parameters, pname, furtherPath):
        """Get the next item on the path

        Should return the item corresponding to 'name' or raise
        Zope.Exceptions.NotFoundError where appropriate.

        The parameters provided, are passed as a sequence of
        name, value items.  The 'pname' argument has the original name
        before parameters were removed. 

        furtherPath is a list of names still to be traversed. This method is
        allowed to change the contents of furtherPath.
        
        """
