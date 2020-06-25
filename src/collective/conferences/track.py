# -*- coding: utf-8 -*-
import datetime

from collective.conferences import _
from DateTime import DateTime
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.indexer import indexer
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.Five import BrowserView
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import RelationChoice, RelationList
from zope import schema
from zope.interface import Invalid, invariant
from zope.security import checkPermission


class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start or end date is invalid")

class StartBeforeConferenceProgram(Invalid):
    __doc__ = _(u"The start of the track could not be set before the conference program.")

class EndAfterConferenceProgram(Invalid):
    __doc__ = _(u'The end of the track could not be set after the conference program.')


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


    trackstart = schema.Datetime(
            title=_(u"Startdate"),
            description =_(u"Start date"),
            required=False,
        )

    trackend = schema.Datetime(
            title=_(u"Enddate"),
            description =_(u"End date"),
            required=False,
        )

    room = RelationList(
        title=_(u'Choose the room for the track'),
        default=[],
        value_type=RelationChoice(vocabulary='ConferenceRoom'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'room',
        RadioFieldWidget,
    )


    def startTimeTalk(data):
        if data.start is not None:
            talkstart = data.start
            return datetime.datetime.talkstart()

    @invariant
    def validateStartEnd(data):
        if data.trackstart is not None and data.trackend is not None:
            if data.trackstart > data.trackend:
                raise StartBeforeEnd(_(
                    u"The start date must be before the end date."))

    @invariant
    def validateStartNotBeforeProgram(data):
        if data.trackstart is not None:
            catalog = api.portal.get_tool(name='portal_catalog')
            result = catalog.uniqueValuesFor('programstart')
            trackstart = DateTime(data.trackstart).toZone('UTC')
            if DateTime(trackstart) < DateTime(result[0]):
                raise StartBeforeConferenceProgram(
                    _(u"The start date could not be set before the begin of the conference program."))


    @invariant
    def validateEndNotAfterProgram(data):
        if data.trackend is not None:
            catalog = api.portal.get_tool(name='portal_catalog')
            result = catalog.uniqueValuesFor('programend')
            trackend = DateTime(data.trackend).toZone('UTC')
            if DateTime(trackend) > DateTime(result[0]):
                raise EndAfterConferenceProgram(
                    _(u"The end date couldn't be set after the end of the conference program."))


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


    def talks_workshops(self):
        tracktitle=self.context.title
        talks_workshops = api.content.find(depth=3,
                                           portal_type=('collective.conferences.talk',
                                                        'collective.conferences.workshop'),
                                           conferencetrack=tracktitle,
                                           review_state='published',
                                           sort_on='orderintrack')
        return [x.getObject() for x in talks_workshops]



    def trackRoom(self):
        results = []
        for rel in self.context.room:
            if rel.isBroken():
                # skip broken relations
                continue
            obj = rel.to_object
            if api.user.has_permission('View', obj=obj):
                results.append(obj)
        return IContentListing(results)
