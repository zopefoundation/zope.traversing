##############################################################################
#
# Copyright (c) 2005 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Traversing test fixtures

$Id$
"""
__docformat__ = "reStructuredText"

import zope.component
import zope.interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

def browserView(for_, name, factory, providing=zope.interface.Interface):
    zope.component.provideAdapter(factory, (for_, IDefaultBrowserLayer),
                                  providing, name=name)

def browserResource(name, factory, providing=zope.interface.Interface):
    zope.component.provideAdapter(factory, (IDefaultBrowserLayer,),
                                  providing, name=name)
