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

$Id: INamespaceHandler.py,v 1.2 2002/06/10 23:28:17 jim Exp $
"""

from Interface import Interface

class INamespaceHandler(Interface):

    def __call__(name, parameters, pname, object, request):
        """Access a name in a namespace

        The name lookup usually depends on an object and/or a
        request. If an object or request is unavailable, None will be passed.

        The parameters provided, are passed as a sequence of
        name, value items.  The 'pname' argument has the original name
        before parameters were removed. 

        It is not the respoonsibility of the handler to wrap the return value.
        """
