# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.supermodel import model
from Products.Five import BrowserView
from zope import schema
from plone.app.textfield import RichText
import datetime
from zope.interface import invariant, Invalid
from plone.indexer import indexer
from plone.supermodel.directives import primary
from plone import api


from zope.component import createObject
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent
from zope.filerepresentation.interfaces import IFileFactory

from DateTime import DateTime


# from plone.formwidget.autocomplete import AutocompleteFieldWidget
from z3c.form.browser.textlines import TextLinesFieldWidget

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from collective.conferences.track import ITrack




class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start or end date is invalid")


class IProgram(model.Schema):
    """A conference program. Programs can contain Tracks.
    """

    title = schema.TextLine(
            title=_(u"Program name"),
        )

    description = schema.Text(
            title=_(u"Program summary"),
        )

    start = schema.Datetime(
            title=_(u"Start date"),
            required=False,
        )

    end = schema.Datetime(
            title=_(u"End date"),
            required=False,
        )

    primary('details')
    details = RichText(
            title=_(u"Details"),
            description=_(u"Details about the program"),
            required=False,
        )

#    form.widget(organizer=AutocompleteFieldWidget)
#    organizer = schema.Choice(
#            title=_(u"Organiser"),
#            vocabulary=u"plone.principalsource.Users",
#            required=False,
#        )


    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_(
                    u"The start date must be before the end date."))


# @form.default_value(field=IProgram['start'])
#def startDefaultValue(data):
#    # To get hold of the folder, do: context = data.context
#    return datetime.datetime.today() + datetime.timedelta(7)


#@form.default_value(field=IProgram['end'])
#def endDefaultValue(data):
    # To get hold of the folder, do: context = data.context
#    return datetime.datetime.today() + datetime.timedelta(10)

# Indexers


@indexer(IProgram)
def startIndexer(obj):
    if obj.start is None:
        return None
    return DateTime(obj.start.isoformat())
# grok.global_adapter(startIndexer, name="start")


@indexer(IProgram)
def endIndexer(obj):
    if obj.end is None:
        return None
    return DateTime(obj.end.isoformat())
# grok.global_adapter(endIndexer, name="end")


@indexer(IProgram)
def tracksIndexer(obj):
    return obj.tracks
# grok.global_adapter(tracksIndexer, name="Subject")


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

# File representation

class ProgramFileFactory(object):
    """Custom file factory for programs, which always creates a Track.
    """

    def __call__(self, name, contentType, data):
        track = createObject('collective.conferences.track')
        notify(ObjectCreatedEvent(track))
        return track
