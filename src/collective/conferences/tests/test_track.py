# -*- coding: utf-8 -*-
from collective.conferences.testing import COLLECTIVE_CONFERENCES_INTEGRATION_TESTING
from collective.conferences.track import ITrack
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class TestTrackIntegration(unittest.TestCase):
    layer = COLLECTIVE_CONFERENCES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal = api.portal.get()
        api.content.create(type='collective.conferences.program', title='test-folder', container=portal)
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_adding(self):
        portal = api.portal.get()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(type='collective.conferences.program', title='program1', container=portal)
        p1 = portal['program1']
        api.content.create(type='collective.conferences.track', title='track1', container=p1)
        s1 = p1['track1']
        self.assertTrue(ITrack.providedBy(s1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.track')
        self.assertNotEqual(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.track')
        schema = fti.lookupSchema()
        self.assertEqual(ITrack, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.track')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ITrack.providedBy(new_object))

    def test_catalog_index_metadata(self):
        self.assertTrue('conferencetrack' in self.portal.portal_catalog.indexes())
        self.assertTrue('track' in self.portal.portal_catalog.schema())


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
