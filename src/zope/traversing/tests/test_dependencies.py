import unittest

from zope.configuration.xmlconfig import XMLConfig
from zope.publisher.browser import TestRequest

from zope.traversing.interfaces import ITraversable


class ZCMLDependencies(unittest.TestCase):

    def test_zcml_can_load(self):
        import zope.traversing
        XMLConfig('configure.zcml', zope.traversing)()

        request = TestRequest()
        res = zope.component.getMultiAdapter(
            (self, request), ITraversable, 'lang')
        import zope.traversing.namespace
        self.assertIsInstance(res, zope.traversing.namespace.lang)
        self.assertIs(res.context, self)
