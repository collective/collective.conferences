# -*- coding: utf-8 -*-
from collective.conferences.program import endDefaultValue
from collective.conferences.program import IProgram
from collective.conferences.program import StartBeforeEnd
from collective.conferences.program import startDefaultValue
from collective.conferences.testing import COLLECTIVE_CONFERENCES_INTEGRATION_TESTING
from collective.conferences.track import ITrack
from DateTime import DateTime
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility
from zope.filerepresentation.interfaces import IFileFactory

import datetime
import unittest


class MockProgram(object):
    pass


class TestProgramUnit(unittest.TestCase):

    def test_start_defaults(self):
        data = MockProgram()
        default_value = startDefaultValue(data)
        today = datetime.datetime.today()
        delta = default_value - today
        self.assertEqual(6, delta.days)

    def test_end_default(self):
        data = MockProgram()
        default_value = endDefaultValue(data)
        today = datetime.datetime.today()
        delta = default_value - today
        self.assertEqual(9, delta.days)

    def test_validate_invariants_ok(self):
        data = MockProgram()
        data.start = datetime.datetime(2009, 1, 1)
        data.end = datetime.datetime(2009, 1, 2)

        try:
            IProgram.validateInvariants(data)
        except:
            self.fail()

    def test_validate_invariants_fail(self):
        data = MockProgram()
        data.start = datetime.datetime(2009, 1, 2)
        data.end = datetime.datetime(2009, 1, 1)

        try:
            IProgram.validateInvariants(data)
            self.fail()
        except StartBeforeEnd:
            pass

    def test_validate_invariants_edge(self):
        data = MockProgram()
        data.start = datetime.datetime(2009, 1, 2)
        data.end = datetime.datetime(2009, 1, 2)

        try:
            IProgram.validateInvariants(data)
        except:
            self.fail()


class TestProgramIntegration(unittest.TestCase):

    layer = COLLECTIVE_CONFERENCES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_adding(self):
        self.folder.invokeFactory('collective.conferences.program', 'program1')
        p1 = self.folder['program1']
        self.assertTrue(IProgram.providedBy(p1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.conferences.program')
        self.assertNotEquals(None, fti)

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
        self.folder.invokeFactory('collective.conferences.program', 'program1')
        p1 = self.folder['program1']
        view = p1.restrictedTraverse('@@view')
        tracks = view.tracks()
        self.assertEqual(0, len(tracks))

    def test_start_end_dates_indexed(self):
        self.folder.invokeFactory('collective.conferences.program', 'program1')
        p1 = self.folder['program1']
        p1.start = datetime.datetime(2009, 1, 1, 14, 00)
        p1.end = datetime.datetime(2009, 1, 2, 15, 00)
        p1.reindexObject()

        result = self.portal.portal_catalog(path='/'.join(p1.getPhysicalPath()))

        self.assertEqual(1, len(result))
        self.assertEqual(result[0].start, DateTime('2009-01-01T14:01:00'))
        self.assertEqual(result[0].end, DateTime('2009-01-02T15:02:00'))

    def test_tracks_indexed(self):
        self.folder.invokeFactory('collective.conferences.program', 'program1')
        p1 = self.folder['program1']
        p1.tracks = ['Track 1', 'Track 2']
        p1.reindexObject()

        result = self.portal.portal_catalog(Subject='Track 2')

        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), p1.absolute_url())

    def test_file_factory(self):
        self.folder.invokeFactory('collective.conferences.program', 'p1')
        p1 = self.folder['p1']
        fileFactory = IFileFactory(p1)
        newObject = fileFactory('new-track', 'text/plain', 'dummy')
        self.assertTrue(ITrack.providedBy(newObject))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
