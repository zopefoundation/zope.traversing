##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
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
$Id: IPhysicallyLocatable.py,v 1.1 2002/07/11 18:21:34 jim Exp $
"""

from Interface import Interface

class IPhysicallyLocatable(Interface):
    """Objects that have a physical location in a containment hierarchy.
    """

    def getPhysicalRoot():
        """Return the physical root object
        """

    def getPhysicalPath():
        """Return the physical path to the object as a sequence of names.
        """

__doc__ = IPhysicallyLocatable.__doc__ + __doc__
