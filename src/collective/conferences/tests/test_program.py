# -*- coding: utf-8 -*-
from collective.conferences.program import endDefaultValue
from collective.conferences.program import IProgram
from collective.conferences.program import startDefaultValue
from collective.conferences.testing import COLLECTIVE_CONFERENCES_INTEGRATION_TESTING
from DateTime import DateTime
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import datetime
import unittest


class MockProgram(object):
    pass


class TestProgramUnit(unittest.TestCase):

    def test_start_defaults(self):
        default_value = startDefaultValue()
        today = datetime.datetime.today()
        delta = default_value - today
        self.assertEqual(13, delta.days)

    def test_end_default(self):
        default_value = endDefaultValue()
        today = datetime.datetime.today()
        delta = default_value - today
        self.assertEqual(16, delta.days)


class TestProgramIntegration(unittest.TestCase):
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
        api.content.create(type='collective.conferences.program', title='program1', container=portal)
        p1 = portal['program1']
        self.assertTrue(IProgram.providedBy(p1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.program')
        self.assertNotEqual(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.program')
        schema = fti.lookupSchema()
        self.assertEqual(IProgram, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.program')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IProgram.providedBy(new_object))

    def test_view(self):
        portal = api.portal.get()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(type='collective.conferences.program', title='program1', container=portal)
        p1 = portal['program1']
        view = p1.restrictedTraverse('@@view')
        tracks = view.tracks()
        self.assertEqual(0, len(tracks))

    def test_start_end_dates_indexed(self):
        portal = api.portal.get()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(type='collective.conferences.program', title='program1', container=portal)
        p1 = portal['program1']
        p1.start = datetime.datetime(2009, 1, 1, 14, 00)
        p1.end = datetime.datetime(2009, 1, 2, 15, 00)
        p1.reindexObject()

        result = self.portal.portal_catalog(path='/'.join(p1.getPhysicalPath()))

        self.assertEqual(1, len(result))
        self.assertEqual(DateTime(result[0].start), DateTime('2009-01-01T14:00:00').toZone('UTC'))
        self.assertEqual(DateTime(result[0].end), DateTime('2009-01-02T15:00:00').toZone('UTC'))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
