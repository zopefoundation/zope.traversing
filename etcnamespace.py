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

$Id: etcnamespace.py,v 1.2 2002/12/25 14:13:26 jim Exp $
"""
from zope.app.applicationcontrol.applicationcontrol \
     import applicationController
from zope.app.traversing.namespaces import provideNamespaceHandler
from zope.app.traversing.exceptions import UnexpectedParameters
from zope.exceptions import NotFoundError

from zope.app.content.folder import RootFolder

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
