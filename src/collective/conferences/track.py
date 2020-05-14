# -*- coding: utf-8 -*-
from collective.conferences import _
from zope import schema
from plone.supermodel import model
from Products.Five import BrowserView
from plone.supermodel.directives import primary

import datetime

from zope.interface import invariant, Invalid
from DateTime import DateTime
from plone.indexer import indexer



from zope.security import checkPermission

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationChoice


from Products.CMFCore.utils import getToolByName

from collective.conferences.room import IRoom







class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start or end date is invalid")

#class StartBeforeConferenceProgram(Invalid):
#    __doc__ = _(u"The start of the track could not before the conference program.")


class ITrack(model.Schema):
    """A conference track. Tracks are managed inside Programs.
    """

    title = schema.TextLine(
            title=_(u"Title"),
            description=_(u"Track title"),
        )

    description = schema.Text(
            title=_(u"Track summary"),
        )

    primary('details')
    details = RichText(
            title=_(u"Track details"),
            required=False
        )


    start = schema.Datetime(
            title=_(u"Startdate"),
            description =_(u"Start date"),
            required=False,
        )

    end = schema.Datetime(
            title=_(u"Enddate"),
            description =_(u"End date"),
            required=False,
        )
    # use an autocomplete selection widget instead of the default content tree
#    form.widget(room=AutocompleteFieldWidget)
#    room = RelationChoice(
#            title=_(u"Room"),
#            source=ObjPathSourceBinder(object_provides=IRoom.__identifier__),
#            required=False,
#        )



#    room = schema.TextLine(
#            title= _(u"Room"),
#        )

    def startTimeTalk(data):
        if data.start is not None:
            talkstart = data.start
            return datetime.datetime.talkstart()

    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_(
                    u"The start date must be before the end date."))

#    @invariant
#   def validateStartNotBeforeProgram(data):
#        if data.start is not None:
#            startprogram = datetime.date (aq_parent (data.start))
#            if data.start < datetime(startprogram):
#                raise StartBeforeConferenceProgram(_(
#                    u"The start date could not before the begin of the conference program."))

# @indexer(ITrack)
# def roomsInde xer(obj):
#    return obj.rooms
#grok.global_adapter(roomsIndexer, name="Subject")

#def setdates(item):
#    if not item.track:
#        return
#    catalog = component.getUtility(ICatalog)
#    intids = component.getUtility(IIntIds)
#    items = [intids.queryObject(rel.from_id) for rel in catalog.findRelations({'to_id': intids.getId(item.track.to_object),
#                                                                                #'from_interfaces_flattened': ITalk
#                                                                                })]
#    start = item.track.to_object.start
#    for t in items:
#        t.startitem=start
#        t.enditem=t.startitem + datetime.timedelta(minutes=int(t.length))
#        start = t.enditem


def trackmodified(track, event):
   print ("track modified")

class TrackView(BrowserView):

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)

    def talks(self):
        catalog = getToolByName(self.context, "portal_catalog")
        talks = catalog.searchResults(
            path=dict(query='/'.join(self.context.getPhysicalPath()),
            depth=1),
            sort_on='getObjPositionInParent')
        return [x.getObject() for x in talks]
