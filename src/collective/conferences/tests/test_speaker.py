# -*- coding: utf-8 -*-
from collective.conferences.testing import COLLECTIVE_CONFERENCES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestPresenterIntegration(unittest.TestCase):
    layer = COLLECTIVE_CONFERENCES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal = api.portal.get()
        api.content.create(type='collective.conferences.speakerfolder', title='test-folder', container=portal)
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
