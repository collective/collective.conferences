# -*- coding: utf-8 -*-
from collective.conferences.attendee import IAttendee
from collective.conferences.testing import COLLECTIVE_CONFERENCES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class TestAttendeeIntegration(unittest.TestCase):
    layer = COLLECTIVE_CONFERENCES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal = api.portal.get()
        api.content.create(type='collective.conferences.attendeefolder', title='test-folder', container=portal)
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_adding(self):
        portal = api.portal.get()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(type='collective.conferences.attendeefolder', title='Attendees', container=portal)
        p1 = portal['attendees']
        api.content.create(type='collective.conferences.attendee', title='test-attendee', container=p1)
        s1 = p1['test-attendee']
        self.assertTrue(IAttendee.providedBy(s1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.attendee')
        self.assertNotEqual(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.attendee')
        schema = fti.lookupSchema()
        self.assertEqual(IAttendee, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.attendee')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IAttendee.providedBy(new_object))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
