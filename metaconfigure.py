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
"""Renderer configuration code

$Id: metaconfigure.py,v 1.1 2003/08/02 18:17:25 srichter Exp $
"""
from namespace import provideNamespaceHandler

def traversalNamespace(_context, name, handler):
    _context.action(
        discriminator=("traversalNamespace", name),
        callable=provideNamespaceHandler,
        args=(name, handler) )

