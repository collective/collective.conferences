# -*- coding: utf-8 -*-
from collective.conferences import _
from collective.conferences.common import allowedconferenceimageextensions
from collective.conferences.common import validateEmail
from collective.conferences.common import validateimagefileextension
from collective.conferences.common import validatePhoneNumber
from plone import api
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from zope import schema


class IConferenceSpeaker(model.Schema):
    """A conference speaker or leader of a workshop. Speaker can be added anywhere.
    """

    lastname = schema.TextLine(
        title=_(safe_unicode('Last name')),
        required=True,
    )

    firstname = schema.TextLine(
        title=_(safe_unicode('First name')),
        required=True,
    )

    street = schema.TextLine(
        title=_(safe_unicode('Street')),
        description=_(safe_unicode(
            'For those requiring visa, please add your full postal address details')),
        required=False,
    )

    city = schema.TextLine(
        title=_(safe_unicode('City')),
        description=_(safe_unicode(
            'For those requiring visa, please add your full postal address details')),
        required=False,
    )

    postalcode = schema.TextLine(
        title=_(safe_unicode('Postal Code')),
        description=_(safe_unicode(
            'For those requiring visa, please add your full postal address details')),
        required=False,
    )

    country = schema.TextLine(
        title=_(safe_unicode('Country')),
        description=_(safe_unicode(
            'For those requiring visa, please add your full postal address details')),
        required=False,
    )

    email = schema.ASCIILine(
        title=_(safe_unicode('Your email address')),
        constraint=validateEmail,
        required=True,
    )

    telephonenumber = schema.TextLine(
        title=_(safe_unicode('Telephone Number')),
        description=_(safe_unicode(
            'Please fill in your telephone number so that we could get in contact with you by phone if necessary.')),
        constraint=validatePhoneNumber,
        required=False,
    )
    mobiletelepone = schema.TextLine(
        title=_(safe_unicode('Mobile Telephone Number')),
        description=_(safe_unicode(
            'Please fill in your mobile telephone number so that we could get in contact with you '
            'during the conference.')),
        constraint=validatePhoneNumber,
        required=True,
    )

    organisation = schema.TextLine(
        title=_(safe_unicode('Organisation')),
        required=False,
    )

    description = schema.Text(
        title=_(safe_unicode('A short bio')),
        required=True,
    )

    bio = RichText(
        title=_(safe_unicode('Bio')),
        required=False,
    )

    directives.mode(speakerpicture='display')
    speakerpicture = schema.TextLine(
        title=_(safe_unicode(
            'The following file extensions are allowed for the picture '
            'files (upper case and lower case and mix of both):')),
        defaultFactory=allowedconferenceimageextensions,
    )

    picture = NamedBlobImage(
        title=_(safe_unicode('Picture')),
        description=_(safe_unicode('Please upload an image')),
        constraint=validateimagefileextension,
        required=False,
    )


def notifyUser(self, event):
    subject = 'Is this you?'
    message = 'A speaker / leader of a workshop called {0} was added here {1}. If ' \
              'this is you, everything is fine.'.format(self.title, self.absolute_url())
    try:
        user = api.user.get_current()
        sender = api.portal.get_registry_record(
            'plone.email_from_address')
        email = user.getProperty('email')

        api.portal.send_email(
            recipient='{0}'.format(email),
            sender='{0}'.format(sender),
            subject='{0}'.format(subject),
            body='{0}'.format(message))

    except Exception:
        sender = self.title
        email = self.email

        api.portal.send_email(
            recipient='{0}'.format(email),
            sender='{0}'.format(sender),
            subject='{0}'.format(subject),
            body='{0}'.format(message))


class ConferenceSpeakerView(BrowserView):

    def talks_of_speaker(self):
        catalog = api.portal.get_tool(name='portal_catalog')

        # execute a search
        results = catalog(speakertalk='Talk 1')
        # examine the results
        for brain in results:
            url = brain.getURL()

        return url

    def talks_of_speaker2(self):
        catalog = api.portal.get_tool(name='portal_catalog')

        # execute a search
        results = catalog(portal_type='collective.conferences.talk',
                          review_state='published')
        # examine the results
        for brain in results:
            title = brain.Title

        return title

    def speakertalks(self):

        speakername = self.context.title
        results = api.content.find(portal_type='collective.conferences.talk',
                                   review_state='published',
                                   presenters=speakername)

        objects = []

        for brain in results:
            objects.append(brain)

        return objects

    def speakerworkshops(self):

        speakername = self.context.title
        results = api.content.find(portal_type='collective.conferences.workshop',
                                   review_state='published',
                                   workshopleader=speakername)

        objects = []

        for brain in results:
            objects.append(brain)
