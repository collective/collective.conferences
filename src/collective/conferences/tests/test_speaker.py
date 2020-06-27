# -*- coding: utf-8 -*-
from collective.conferences.conferencespeaker import IConferenceSpeaker
from collective.conferences.conferencespeaker import notifyUser
from collective.conferences.testing import COLLECTIVE_CONFERENCES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.mocktestcase import MockTestCase
from zope.app.container.contained import ObjectAddedEvent
from zope.component import createObject
from zope.component import queryUtility

import unittest


class TestPresenterMock(MockTestCase):

    def test_notify_user(self):
        # dummy conferencespeaker
        conferencespeaker = self.create_dummy(
            __parent__=None,
            __name__=None,
            title='Jim',
            absolute_url=lambda: 'http://example.org/conferencespeaker',
        )

        # dummy event
        event = ObjectAddedEvent(conferencespeaker)

        # search result for acl_users
        user_info = [{'email': 'jim@example.org', 'id': 'jim'}]

        # email data
        message = 'A speaker called Jim was added here http://example.org/conferencespeaker'
        email = 'jim@example.org'
        sender = 'test@example.org'
        subject = 'Is this you?'

        # mock tools/portal

        portal_mock = self.mocker.mock()
        self.expect(portal_mock.getProperty('email_from_address')).result('test@example.org')

        portal_url_mock = self.mocker.mock()
        self.mock_tool(portal_url_mock, 'portal_url')
        self.expect(portal_url_mock.getPortalObject()).result(portal_mock)

        acl_users_mock = self.mocker.mock()
        self.mock_tool(acl_users_mock, 'acl_users')
        self.expect(acl_users_mock.searchUsers(fullname='Jim')).result(user_info)

        mail_host_mock = self.mocker.mock()
        self.mock_tool(mail_host_mock, 'MailHost')
        self.expect(mail_host_mock.secureSend(message, email, sender, subject))

        # put mock framework into replay mode
        self.replay()

        # call the method under test
        notifyUser(conferencespeaker, event)

        # we could make additional assertions here, e.g. if the function
        # returned something. The mock framework will verify the assertions
        # about expected call sequences.


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
        portal=api.portal.get()
        testfolder=portal['test-folder']
        api.content.create(container=testfolder, type='collective.conferences.conferencespeaker', title='conferencespeaker1')
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
