# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.app.textfield import RichText
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.Five import BrowserView
from zope import schema
from zope.security import checkPermission


# from collective.conferences.attendee import IAttendee

class IAttendeefolder(model.Schema):
    """A attendee folder. The attendee of the conference are created in the folder.
    """

    title = schema.TextLine(
        title=_(u'Name of the attendee folder'),
    )

    description = schema.Text(
        title=_(u'attendee folder description'),
        required=False,
    )

    primary('moreinformation')
    moreinformation = RichText(
        title=_(u'Information about registration process'),
        required=False,
    )


class AttendeefolderView(BrowserView):

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)
