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
"""

Revision information:
$Id: ParameterParsing.py,v 1.2 2002/06/10 23:28:17 jim Exp $
"""

import re

namespace_pattern = re.compile('[+][+]([a-zA-Z0-9_]+)[+][+]')

def parameterizedNameParse(name):
    """Parse a name with parameters, including namespace parameters.
    
    Return:
    
    - namespace, or None if there isn't one.
    
    - unparameterized name
    
    - sequence of parameters, as name-value pairs.
    """

    ns = ''
    if name[:2] == '@@':
        ns = 'view'
        name = name[2:]
    else:
        match = namespace_pattern.match(name)
        if match:
            prefix, ns = match.group(0, 1)
            name = name[len(prefix):]

    return ns, name, ()
