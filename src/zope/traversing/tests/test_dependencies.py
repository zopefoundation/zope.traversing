import os
import unittest

import zope.component
from zope.app.testing import functional
from zope.publisher.browser import TestRequest

from zope.traversing.interfaces import ITraversable
import zope.traversing.namespace


TraversingLayer = functional.ZCMLLayer(
    os.path.join(os.path.dirname(__file__), 'ftest_zcml_dependencies.zcml'),
    __name__, 'TraversingLayer', allow_teardown=True)


class ZCMLDependencies(functional.BrowserTestCase):

    def test_zcml_can_load_with_only_zope_component_meta(self):
        # this is just an example.  It is supposed to show that the
        # configure.zcml file has loaded successfully, with only loading the
        # meta.zcml from zope.component.
        request = TestRequest()
        res = zope.component.getMultiAdapter(
            (self, request), ITraversable, 'lang')
        self.failUnless(isinstance(res, zope.traversing.namespace.lang))
        self.failUnless(res.context is self)

def test_suite():
    suite = unittest.TestSuite()
    ZCMLDependencies.layer = TraversingLayer
    suite.addTest(unittest.makeSuite(ZCMLDependencies))
    return suite


if __name__ == '__main__':
    unittest.main()
