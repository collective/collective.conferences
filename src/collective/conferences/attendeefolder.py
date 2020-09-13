# -*- coding: utf-8 -*-
from collective.conferences import _
from plone import api
from plone.app.textfield import RichText
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from zope import schema


# from collective.conferences.attendee import IAttendee

class IAttendeefolder(model.Schema):
    """A attendee folder. The attendee of the conference are created in the folder.
    """

    title = schema.TextLine(
        title=_(safe_unicode('Name of the attendee folder')),
    )

    description = schema.Text(
        title=_(safe_unicode('attendee folder description')),
        required=False,
    )

    primary('moreinformation')
    moreinformation = RichText(
        title=_(safe_unicode('Information about registration process')),
        required=False,
    )


class AttendeefolderView(BrowserView):

    def canRequestReview(self):
        return api.user.has_permission('cmf.RequestReview', obj=self.context)
