# -*- coding: utf-8 -*-
from collective.conferences.speakerfolder import ISpeakerfolder
from collective.conferences.testing import COLLECTIVE_CONFERENCES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class TestSpeakerfolderIntegration(unittest.TestCase):
    layer = COLLECTIVE_CONFERENCES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal = api.portal.get()
        api.content.create(type='Folder', title='test-folder', container=portal)
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_adding(self):
        portal = api.portal.get()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(type='collective.conferences.speakerfolder', title='speakers', container=portal)
        p1 = portal['speakers']
        self.assertTrue(ISpeakerfolder.providedBy(p1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.speakerfolder')
        self.assertNotEqual(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.speakerfolder')
        schema = fti.lookupSchema()
        self.assertEqual(ISpeakerfolder, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.speakerfolder')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ISpeakerfolder.providedBy(new_object))

    def test_textedit(self):
        portal = api.portal.get()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(type='collective.conferences.speakerfolder', title='speakers', container=portal)
        text = 'The list of the conference speakers'
        context = portal['speakers']
        context.description = text
        self.assertEqual(context.description, text)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
