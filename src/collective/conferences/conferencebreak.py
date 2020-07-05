# -*- coding: utf-8 -*-
from collective.conferences import _
from collective.conferences.common import endDefaultValue
from collective.conferences.common import startDefaultValue
from plone import api
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.autoform.directives import write_permission
from plone.dexterity.browser.view import DefaultView
from plone.supermodel import model
from plone.supermodel.directives import primary
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IConferencebreak(model.Schema):
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Conference break title'),
    )

    description = schema.Text(
        title=_(u'Conference break summary'),
        required=False,
    )

    primary('details')
    details = RichText(
        title=_(u'Conference break details'),
        required=False,
    )

    write_permission(startitem='collective.conferences.ModifyTalktime')
    startitem = schema.Datetime(
        title=_(u'Startdate'),
        description=_(u'Start date'),
        defaultFactory=startDefaultValue,
        required=False,
    )

    write_permission(enditem='collective.conferences.ModifyTalktime')
    enditem = schema.Datetime(
        title=_(u'Enddate'),
        description=_(u'End date'),
        defaultFactory=endDefaultValue,
        required=False,
    )
    write_permission(breaklength='collective.conferences.ModifyTalktime')
    directives.widget(breaklength=RadioFieldWidget)
    breaklength = schema.List(
        title=_(u'Length'),
        value_type=schema.Choice(source='BreakLength'),
        required=True,
    )

    write_permission(conferencetrack='collective.conferences.ModifyTalktime')
    conferencetrack = RelationList(
        title=_(u'Choose the track for this break'),
        default=[],
        value_type=RelationChoice(vocabulary='ConferenceTrack'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'conferencetrack',
        RadioFieldWidget,
    )

    positionintrack = schema.Int(
        title=_(u'Position In The Track'),
        description=_(u'Choose a number for the order in the track'),
        required=False,
    )


class ConferencebreakView(DefaultView):

    def canRequestReview(self):
        return api.user.has_permission('cmf.RequestReview', obj=self.context)
