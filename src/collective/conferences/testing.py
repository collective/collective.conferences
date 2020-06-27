# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.conferences


class CollectiveConferencesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.conferences)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.conferences:default')


COLLECTIVE_CONFERENCES_FIXTURE = CollectiveConferencesLayer()


COLLECTIVE_CONFERENCES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CONFERENCES_FIXTURE,),
    name='CollectiveConferencesLayer:IntegrationTesting',
)


COLLECTIVE_CONFERENCES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CONFERENCES_FIXTURE,),
    name='CollectiveConferencesLayer:FunctionalTesting',
)


COLLECTIVE_CONFERENCES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_CONFERENCES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveConferencesLayer:AcceptanceTesting',
)
