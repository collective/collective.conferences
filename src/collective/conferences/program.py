# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.conferences import _
from collective.conferences.common import endDefaultValue
from collective.conferences.common import startDefaultValue
from collective.conferences.track import ITrack
from plone import api
from plone.app.textfield import RichText
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.validation import V_REQUIRED  # noqa
from zope import schema
from zope.interface import Invalid
from zope.interface import invariant


class StartBeforeEnd(Invalid):
    __doc__ = _(safe_unicode('The start or end date is invalid'))


class IProgram(model.Schema):
    """A conference program. Programs can contain Tracks.
    """

    title = schema.TextLine(
        title=_(safe_unicode('Program name')),
    )

    description = schema.Text(
        title=_(safe_unicode('Program summary')),
    )

    start = schema.Datetime(
        title=_(safe_unicode('Start date')),
        required=False,
        defaultFactory=startDefaultValue,
    )

    end = schema.Datetime(
        title=_(safe_unicode('End date')),
        required=False,
        defaultFactory=endDefaultValue,
    )

    primary('details')
    details = RichText(
        title=_(safe_unicode('Details')),
        description=_(safe_unicode('Details about the program')),
        required=False,
    )

    directives.widget(organizer=AjaxSelectFieldWidget)
    organizer = schema.Choice(
        title=_(safe_unicode('Organiser')),
        vocabulary=safe_unicode('plone.app.vocabularies.Users'),
        required=False,
    )

    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_(
                    safe_unicode(
                        'The start date must be before the end date.')))


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

    def track_list(self):
        return api.content.find(depth=3, portal_type='collective.conferences.track')

    def trackRoom(self, track):
        path = track.getPath()
        catalog = api.portal.get_tool('portal_catalog')
        return catalog.getIndexDataForUID(path).get('trackroom')[0]

    def track_talks_workshops(self, track):
        tracktitle = track.Title
        talks_workshops = api.content.find(depth=3,
                                           portal_type=('collective.conferences.talk',
                                                        'collective.conferences.workshop',
                                                        'collective.conferences.conferencebreak'),
                                           conferencetrack=tracktitle,
                                           review_state='published',
                                           sort_on='orderintrack')

        return [z.getObject() for z in talks_workshops]
