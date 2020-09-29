# -*- coding: utf-8 -*-
from collective.conferences import _
from datetime import timedelta
from DateTime import DateTime
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import Invalid
from zope.interface import invariant

import transaction


class StartBeforeEnd(Invalid):
    __doc__ = _(safe_unicode('The start or end date is invalid'))


class StartBeforeConferenceProgram(Invalid):
    __doc__ = _(safe_unicode('The start of the track could not be set before the conference program.'))


class EndAfterConferenceProgram(Invalid):
    __doc__ = _(safe_unicode('The end of the track could not be set after the conference program.'))


class ITrack(model.Schema):
    """A conference track. Tracks are managed inside Programs.
    """

    title = schema.TextLine(
        title=_(safe_unicode('Title')),
        description=_(safe_unicode('Track title')),
    )

    description = schema.Text(
        title=_(safe_unicode('Track summary')),
    )

    primary('details')
    details = RichText(
        title=_(safe_unicode('Track details')),
        required=False,
    )

    trackstart = schema.Datetime(
        title=_(safe_unicode('Startdate')),
        description=_(safe_unicode('Start date')),
        required=False,
    )

    trackend = schema.Datetime(
        title=_(safe_unicode('Enddate')),
        description=_(safe_unicode('End date')),
        required=False,
    )

    room = RelationList(
        title=_(safe_unicode('Choose the room for the track')),
        default=[],
        value_type=RelationChoice(vocabulary='ConferenceRoom'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'room',
        RadioFieldWidget,
    )

    @invariant
    def validateStartEnd(data):
        if data.trackstart is not None and data.trackend is not None:
            if data.trackstart > data.trackend:
                raise StartBeforeEnd(_(
                    safe_unicode(
                        'The start date must be before the end date.')))

    @invariant
    def validateStartNotBeforeProgram(data):
        if data.trackstart is not None:
            catalog = api.portal.get_tool(name='portal_catalog')
            result = catalog.uniqueValuesFor('programstart')
            trackstart = DateTime(data.trackstart).toZone('UTC')
            if DateTime(trackstart) < DateTime(result[0]):
                raise StartBeforeConferenceProgram(
                    _(safe_unicode(
                        'The start date could not be set before the begin of the conference program.')))

    @invariant
    def validateEndNotAfterProgram(data):
        if data.trackend is not None:
            catalog = api.portal.get_tool(name='portal_catalog')
            result = catalog.uniqueValuesFor('programend')
            trackend = DateTime(data.trackend).toZone('UTC')
            if DateTime(trackend) > DateTime(result[0]):
                raise EndAfterConferenceProgram(
                    _(safe_unicode("The end date couldn't be set after the end of the conference program.")))


class TrackView(BrowserView):

    def canRequestReview(self):
        return api.user.has_permission('cmf.RequestReview', obj=self.context)

    def talks_workshops(self):
        tracktitle = self.context.title
        talks_workshops = api.content.find(depth=3,
                                           portal_type=('collective.conferences.talk',
                                                        'collective.conferences.workshop',
                                                        'collective.conferences.conferencebreak'),
                                           conferencetrack=tracktitle,
                                           review_state='published',
                                           sort_on='orderintrack')
        start = self.context.trackstart
        for x in talks_workshops:
            x.getObject().startitem = start
            talklength = x.getObject().talklength[0]
            delta = timedelta(minutes=int(talklength))
            x.getObject().enditem = start + delta
            transaction.commit()
            start += delta
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
