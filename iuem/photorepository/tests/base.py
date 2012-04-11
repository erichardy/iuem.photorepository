import unittest2 as unittest
from zope import interface
from plone.app import testing
from iuem.photorepository.tests import layer
from iuem.photorepository.tests import utils

class UnitTestCase(unittest.TestCase):
    
    def setUp(self):
        from ZPublisher.tests.testPublish import Request
        from zope.annotation.interfaces import IAttributeAnnotatable
        from iuem.photorepository.browser.interfaces import ILayer
        super(UnitTestCase, self).setUp()
        self.context = utils.FakeContext()
        self.request = Request()
        interface.alsoProvides(self.request,
                               (IAttributeAnnotatable,ILayer))

class TestCase(unittest.TestCase):

    layer = layer.INTEGRATION

    def setUp(self):
        from zope.annotation.interfaces import IAttributeAnnotatable
        from iuem.photorepository.browser.interfaces import ILayer
        interface.alsoProvides(self.layer['request'],
                               (IAttributeAnnotatable,ILayer))
        super(TestCase, self).setUp()
        self.portal = self.layer['portal']
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']


class FunctionalTestCase(unittest.TestCase):

    layer = layer.FUNCTIONAL

    def setUp(self):
        from zope.annotation.interfaces import IAttributeAnnotatable
        from iuem.photorepository.browser.interfaces import ILayer
        interface.alsoProvides(self.layer['request'],
                               (IAttributeAnnotatable,ILayer))
        self.portal = self.layer['portal']
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

def build_test_suite(test_classes):
    suite = unittest.TestSuite()
    for klass in test_classes:
        suite.addTest(unittest.makeSuite(klass))
    return suite
