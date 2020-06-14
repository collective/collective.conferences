# -*- coding: utf-8 -*-
from collective.conferences import _
from zope.interface import Invalid
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from Products.Five import BrowserView
from zope import schema
from plone import api

import re




checkEmail = re.compile(
     r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}").match
     
def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(u"Invalid email address"))
    return True

class IConferenceSpeaker(model.Schema):
    """A conference speaker or leader of a workshop. Speaker can be added anywhere.
    """

    lastname= schema.TextLine(
            title=_(u"Last name"),
        )
    
    firstname = schema.TextLine(
             title=_(u"First name"),
             required=True,
        )
  
    street = schema.TextLine(
            title=_(u"Street"),
            description=_(u"For those requiring visa, please add your full postal address details"),
            required=False,
        )
    
    city = schema.TextLine(
            title=_(u"City"),
            description=_(u"For those requiring visa, please add your full postal address details"),
            required=False,
        )
    
    postalcode = schema.TextLine(
                 title=_(u"Postal Code"),
                 description=_(u"For those requiring visa, please add your full postal address details"),
                 required=False,
        )
    
    country = schema.TextLine(
              title=_(u"Country"),
              description=_(u"For those requiring visa, please add your full postal address details"),
              required=False,
        )

    email = schema.ASCIILine(
            title=_(u"Your email address"),
            constraint=validateEmail,
            required=True,
        )

    telephonenumber = schema.TextLine(
            title=_(u"Telephone Number"),
            description=_(u"Please fill in your telephone number so that we could get in contact with you by phone if necessary."),
            required=False,
        )
    mobiletelepone = schema.TextLine(
            title=_(u"Mobile Telephone Number"),
            description=_(u"Please fill in your mobile telephone number so that we could get in contact with you during the conference."),
            required=True,
        )
    
    organisation = schema.TextLine(
            title=_(u"Organisation"),
            required=False,
        )

    description = schema.Text(
            title=_(u"A short bio"),
        )
    
    bio = RichText(
            title=_(u"Bio"),
            required=False
        )
    
    picture = NamedBlobImage(
            title=_(u"Picture"),
            description=_(u"Please upload an image"),
            required=False,
        )

def notifyUser(self, event):
    user = api.user.get_current()
    sender = api.portal.get_registry_record(
        'plone.email_from_address')
    email = user.getProperty('email')

    if not sender:
        return

    subject = "Is this you?"
    message = "A speaker /leader of a workshop called %s was added here %s. If this is you, everything is fine." % (self.title, self.absolute_url(),)

    api.portal.send_email(
        recipient='{0}'.format(email),
        sender= '{0}'.format(sender),
        subject='{0}'.format(subject),
        body='{0}'.format(message),)


class ConferenceSpeakerView(BrowserView):

    def talks_of_speaker(self):
        from collective.conferences.talk import ITalk
        context = self.context
        catalog = api.portal.get_tool(name='portal_catalog')

        # execute a search
        results = catalog(speakertalk='Talk 1')
        # examine the results
        for brain in results:
            start = brain.start
            url = brain.getURL()
            obj = brain.getObject()

        return url


    def talks_of_speaker2(self):
        from collective.conferences.talk import ITalk
        context = self.context
        catalog = api.portal.get_tool(name='portal_catalog')

        # execute a search
        results = catalog(portal_type="collective.conferences.talk",
                          review_state="published")
        # examine the results
        for brain in results:
            start = brain.start
            url = brain.getURL()
            obj = brain.getObject()
            title = brain.Title

        return title



    def speakertalks(self):

        speakername = self.context.title
        results  = api.content.find(portal_type="collective.conferences.talk",
                                    review_state="published",
                                    presenters=speakername)

        objects =[]

        for brain in results:
            objects.append(brain)

        return objects