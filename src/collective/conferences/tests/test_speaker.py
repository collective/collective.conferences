# -*- coding: utf-8 -*-
from collective.conferences.conferencespeaker import IConferenceSpeaker
from collective.conferences.testing import COLLECTIVE_CONFERENCES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

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

    def test_adding(self):
        portal = api.portal.get()
        testfolder = portal['test-folder']
        api.content.create(container=testfolder, type='collective.conferences.conferencespeaker',
                           title='conferencespeaker1')
        p1 = self.folder['test-folder/conferencespeaker1']
        self.assertTrue(IConferenceSpeaker.providedBy(p1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.conferencespeaker')
        self.assertNotEqual(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.conferencespeaker')
        schema = fti.lookupSchema()
        self.assertEqual(IConferenceSpeaker, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.conferencespeaker')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IConferenceSpeaker.providedBy(new_object))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
