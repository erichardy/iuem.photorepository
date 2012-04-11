from plone.testing import z2

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting

class Layer(PloneSandboxLayer):
    default_bases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import iuem.photorepository
        self.loadZCML(package=iuem.photorepository)

        # Install product and call its initialize() function
        z2.installProduct(app, 'iuem.photorepository')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'iuem.photorepository:default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'iuem.photorepository')

FIXTURE = Layer()

INTEGRATION = IntegrationTesting(bases=(FIXTURE,),
                        name="iuem.photorepository:Integration")
FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,),
                        name="iuem.photorepository:Functional")
