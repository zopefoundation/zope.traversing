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

$Id: EtcNamespace.py,v 1.5 2002/12/20 19:45:45 jim Exp $
"""
from Zope.App.OFS.ApplicationControl.ApplicationControl \
     import applicationController
from Namespaces import provideNamespaceHandler
from Exceptions import UnexpectedParameters
from Zope.Exceptions import NotFoundError

from Zope.App.OFS.Content.Folder.RootFolder import RootFolder

def etc(name, parameters, pname, ob, request):
    # XXX

    # This is here now to allow us to get service managers from a
    # separate namespace from the content. We add and etc
    # namespace to allow us to handle misc objects.  We'll apply
    # YAGNI for now and hard code this. We'll want something more
    # general later. We were thinking of just calling "get"
    # methods, but this is probably too magic. In particular, we
    # will treat returned objects as sub-objects wrt security and
    # not all get methods may satisfy this assumption. It might be
    # best to introduce some sort of etc registry.

    if parameters:
        raise UnexpectedParameters(parameters)

    if name == 'ApplicationController' and ob.__class__ == RootFolder:
        return applicationController

    if name != 'Services':
        
        raise NotFoundError(ob, pname, request)

    method_name = "getServiceManager"
    method = getattr(ob, method_name, None)
    if method is None: 
        raise NotFoundError(ob, pname, request)

    return method()
