"""This is an integration "unit" test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for 
example.
"""

from iuem.photorepository.tests import base

class TestSetup(base.TestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """

    def setUp(self):
        super(TestSetup, self).setUp()
        self.portal_types = self.portal.portal_types

    def beforeTearDown(self):
        pass

    def test_view_methods(self):
        for t in ('Link', 'Folder', 'Topic'):
            views = self.portal_types.getTypeInfo(t).view_methods
#            self.failUnless("my_view" in views)

def test_suite():
   return base.build_test_suite((TestSetup,))
