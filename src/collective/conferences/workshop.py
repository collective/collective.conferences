# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from collective import dexteritytextindexer
from collective.conferences import _
from collective.conferences.common import endDefaultValue
from collective.conferences.common import startDefaultValue
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.textfield import RichText
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import directlyProvides
from zope.interface import Invalid
from zope.interface import invariant
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def vocabCfPTopics(context):
    # For add forms
    catalog = api.portal.get_tool(name='portal_catalog')
    results = catalog.uniqueValuesFor('callforpaper_topics')
    terms = []
    for value in results:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))

    return SimpleVocabulary(terms)


directlyProvides(vocabCfPTopics, IContextSourceBinder)


class ChooseLicense(Invalid):
    __doc__ = _(safe_unicode(
        'Please choose a license for your talk.'))


class IWorkshop(model.Schema):
    """A conference workshop.
    """

    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Workshop title'),
    )

    description = schema.Text(
        title=_(u'Workshop summary'),
    )

    primary('details')
    details = RichText(
        title=_(u'Workshop details'),
        required=False,
    )

    speaker = RelationList(
        title=_(u'Workshop Leader'),
        default=[],
        value_type=RelationChoice(vocabulary='ConferenceSpeaker'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'speaker',
        SelectFieldWidget,
    )

    dexteritytextindexer.searchable('call_for_paper_topics')
    directives.widget(call_for_paper_topic=RadioFieldWidget)
    call_for_paper_topic = schema.List(
        title=_(u'Choose the topic for your workshop'),
        value_type=schema.Choice(source=vocabCfPTopics),
        required=True,
    )

    directives.widget(planedworkshoplength=RadioFieldWidget)
    planedworkshoplength = schema.List(
        title=_(u'Planed Length'),
        description=_(u"Give an estimation about the time you'd plan for your workshop."),
        value_type=schema.Choice(source='WorkshopLength'),
        required=True,
    )

    directives.widget(license=RadioFieldWidget)
    license = schema.List(
        title=_(u'License Of Your Talk'),
        description=_(u'Choose a license for your talk'),
        value_type=schema.Choice(source='ContentLicense'),
        required=True,
    )

    read_permission(conferencetrack='cmf.ReviewPortalContent')
    write_permission(conferencetrack='cmf.ReviewPortalContent')
    conferencetrack = RelationList(
        title=_(u'Choose the track for this talk'),
        default=[],
        value_type=RelationChoice(vocabulary='ConferenceTrack'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'conferencetrack',
        RadioFieldWidget,
    )

    messagetocommittee = schema.Text(
        title=_(u'Messages to the Program Committee'),
        description=_(
            u'You can give some information to the committee here, e.g. about days you are (not) available to give the workshop'),
        required=False,
    )

    read_permission(workshoplength='cmf.ReviewPortalContent')
    write_permission(workshoplength='cmf.ReviewPortalContent')
    directives.widget(workshoplength=RadioFieldWidget)
    workshoplength = schema.List(
        title=_(u'Workshop Length'),
        description=_(u'Set a time frame for the workshop in minutes.'),
        value_type=schema.Choice(source='WorkshopLength'),
        required=False,
    )

    read_permission(positionintrack='cmf.ReviewPortalContent')
    write_permission(positionintrack='cmf.ReviewPortalContent')
    positionintrack = schema.Int(
        title=_(u'Position In The Track'),
        description=_(u'Choose a number for the order in the track'),
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

    model.fieldset('slides',
                   label=_(u'Slides'),
                   fields=['slides'],
    )

    slides = NamedBlobFile(
        title=_(u'Workshop slides / material'),
        description=_(
            u'Please upload your workshop presentation or material about the content of the workshop '
            u'in front or short after you have given the workshop.'),
        required=False,
    )

    read_permission(reviewNotes='cmf.ReviewPortalContent')
    write_permission(reviewNotes='cmf.ReviewPortalContent')
    reviewNotes = schema.Text(
        title=u'Review notes',
        required=False,
    )

    @invariant
    def validateLicensechoosen(data):
        if not data.license:
            raise ChooseLicense(
                _(safe_unicode('Please choose a license for your talk.'),
                  ),
            )


def newworkshopadded(self, event):
    if api.portal.get_registry_record(
            'plone.email_from_address') is not None:
        contactaddress = api.portal.get_registry_record(
            'plone.email_from_address')
        current_user = api.user.get_current()

        length = self.planedworkshoplength[0]
        cfp = self.call_for_paper_topic[0]
        details = self.details.output

        api.portal.send_email(
            recipient=current_user.getProperty('email'),
            sender=contactaddress,
            subject=safe_unicode('Your Workshop Proposal'),
            body=safe_unicode('You submitted a conference workshop:\n'
                              'title: {0},\n'
                              'summary: {1},\n'
                              'details: {2},\n'
                              'proposed length: {3} minutes\nfor the call for papers '
                              'topic: {4}\nwith the following message to the conference '
                              'committee: {5}\n\n'
                              'Best regards,\n'
                              'The Conference Committee').format(
                self.title, self.description, details,
                length, cfp, self.messagetocommittee),
        )


class WorkshopView(BrowserView):

    def canRequestReview(self):
        return api.user.has_permission('cmf.RequestReview', obj=self.context)

    def workshopLeaders(self):
        results = []
        for rel in self.context.speaker:
            if rel.isBroken():
                # skip broken relations
                continue
            obj = rel.to_object
            if api.user.has_permission('View', obj=obj):
                results.append(obj)
        return IContentListing(results)

    def conferenceTrack(self):
        results = []
        for rel in self.context.conferencetrack:
            if rel.isBroken():
                # skip broken relations
                continue
            obj = rel.to_object
            if api.user.has_permission('View', obj=obj):
                results.append(obj)
        return IContentListing(results)

    def WorkshopRoom(self):

        from collective.conferences.track import ITrack
        parent = aq_parent(aq_inner(self.context))
        if ITrack.providedBy(parent):
            room = parent.room.to_object.title
        else:
            room = ''
        return room
