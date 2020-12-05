# -*- coding: utf-8 -*-
from collective.conferences.testing import COLLECTIVE_CONFERENCES_INTEGRATION_TESTING
from collective.conferences.workshop import IWorkshop
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class TestWorkshopIntegration(unittest.TestCase):
    layer = COLLECTIVE_CONFERENCES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal = api.portal.get()
        api.content.create(type='collective.conferences.twfolder', title='Talks / Workshops', container=portal)
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['talks-workshops']

    def test_adding(self):
        portal = api.portal.get()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(type='collective.conferences.twfolder', title='Talks / Workshops', container=portal)
        p1 = portal['talks-workshops']
        api.content.create(type='collective.conferences.workshop', title='test-workshop', container=p1)
        s1 = p1['test-workshop']
        self.assertTrue(IWorkshop.providedBy(s1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.workshop')
        self.assertNotEqual(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.workshop')
        schema = fti.lookupSchema()
        self.assertEqual(IWorkshop, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.workshop')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IWorkshop.providedBy(new_object))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
