# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.conferences import _
from collective.conferences.track import ITrack
from plone import api
from plone.app.textfield import RichText
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.Five import BrowserView
from zope import schema
from zope.component import createObject
from zope.event import notify
from zope.interface import Invalid
from zope.interface import invariant
from zope.lifecycleevent import ObjectCreatedEvent

import datetime


def startDefaultValue():
    return datetime.datetime.today() + datetime.timedelta(14)


def endDefaultValue():
    return datetime.datetime.today() + datetime.timedelta(17)


class StartBeforeEnd(Invalid):
    __doc__ = _(u'The start or end date is invalid')


class IProgram(model.Schema):
    """A conference program. Programs can contain Tracks.
    """

    title = schema.TextLine(
        title=_(u'Program name'),
    )

    description = schema.Text(
        title=_(u'Program summary'),
    )

    start = schema.Datetime(
        title=_(u'Start date'),
        required=False,
        defaultFactory=startDefaultValue,
    )

    end = schema.Datetime(
        title=_(u'End date'),
        required=False,
        defaultFactory=endDefaultValue
    )

    primary('details')
    details = RichText(
        title=_(u'Details'),
        description=_(u'Details about the program'),
        required=False,
    )

    directives.widget(organizer=AjaxSelectFieldWidget)
    organizer = schema.Choice(
        title=_(u'Organiser'),
        vocabulary=u'plone.app.vocabularies.Users',
        required=False,
    )

    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_(
                    u'The start date must be before the end date.'))


# Views

class ProgramView(BrowserView):

    def tracks(self):
        """Return a catalog search result of tracks to show
        """

        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')

        return catalog(object_provides=ITrack.__identifier__,
                       path='/'.join(context.getPhysicalPath()),
                       sort_order='sortable_title')


class FullprogramView(BrowserView):
    pass

