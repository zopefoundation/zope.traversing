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
"""'traversalNamespace' directive handler

$Id: metadirectives.py,v 1.1 2003/08/02 18:17:25 srichter Exp $
"""
from zope.configuration.fields import GlobalObject, PythonIdentifier
from zope.interface import Interface

class ITraversalNamespaceDirective(Interface):
    """Register a new traversal namespace."""
    
    name = PythonIdentifier(
        title=u"Name",
        description=u"The name under which the namespace will be accessible.",
        required=True)

    handler = GlobalObject(
        title=u"Handler",
        description=u"Specifies the handler component for this namespace.",
        required=True)
