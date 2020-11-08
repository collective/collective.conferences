# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from collective import dexteritytextindexer
from collective.conferences import _
from collective.conferences.common import allowedconferencevideoextensions
from collective.conferences.common import allowedconferenceworkshopmaterialextensions
from collective.conferences.common import allowedconferenceworkshopslideextensions
from collective.conferences.common import endDefaultValue
from collective.conferences.common import quote_chars
from collective.conferences.common import startDefaultValue
from collective.conferences.common import validatelinkedworkshopslidefileextension
from collective.conferences.common import validatevideofileextension
from collective.conferences.common import validateworkshopmaterialfileextension
from collective.conferences.common import validateworshopslidefileextension
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
from z3c.form import validator
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
        'Please choose a license for your workshop.'))


class ChooseCfpTopic(Invalid):
    __doc__ = _(safe_unicode(
        'Please choose a call for paper topic for your workshop.'))


class ChoosePlanedLength(Invalid):
    __doc__ = _(safe_unicode(
        'Please choose a planed length for your workshop.'))


class IWorkshop(model.Schema):
    """A conference workshop.
    """

    title = schema.TextLine(
        title=_(safe_unicode('Title')),
        description=_(safe_unicode('Workshop title')),
    )

    description = schema.Text(
        title=_(safe_unicode('Workshop summary')),
    )

    primary('details')
    details = RichText(
        title=_(safe_unicode('Workshop details')),
        required=False,
    )

    speaker = RelationList(
        title=_(safe_unicode('Workshop Leader')),
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
        title=_(safe_unicode('Choose the topic for your workshop')),
        value_type=schema.Choice(source=vocabCfPTopics),
        required=True,
    )

    directives.widget(planedworkshoplength=RadioFieldWidget)
    planedworkshoplength = schema.List(
        title=_(safe_unicode('Planed Length')),
        description=_(safe_unicode(
            "Give an estimation about the time you'd plan for your workshop.")),
        value_type=schema.Choice(source='WorkshopLength'),
        required=True,
    )

    directives.widget(license=RadioFieldWidget)
    license = schema.List(
        title=_(safe_unicode('License Of Your Talk')),
        description=_(safe_unicode('Choose a license for your workshop')),
        value_type=schema.Choice(source='ContentLicense'),
        required=True,
    )

    read_permission(conferencetrack='cmf.ReviewPortalContent')
    write_permission(conferencetrack='cmf.ReviewPortalContent')
    conferencetrack = RelationList(
        title=_(safe_unicode('Choose the track for this workshop')),
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
        title=_(safe_unicode('Messages to the Program Committee')),
        description=_(safe_unicode(
            'You can give some information to the committee here, e.g. about days you are (not) '
            'available to give the workshop')),
        required=False,
    )

    read_permission(workshoplength='cmf.ReviewPortalContent')
    write_permission(workshoplength='cmf.ReviewPortalContent')
    directives.widget(workshoplength=RadioFieldWidget)
    workshoplength = schema.List(
        title=_(safe_unicode('Workshop Length')),
        description=_(safe_unicode('Set a time frame for the workshop in minutes.')),
        value_type=schema.Choice(source='WorkshopLength'),
        required=False,
    )

    read_permission(positionintrack='cmf.ReviewPortalContent')
    write_permission(positionintrack='cmf.ReviewPortalContent')
    positionintrack = schema.Int(
        title=_(safe_unicode('Position In The Track')),
        description=_(safe_unicode('Choose a number for the order in the track')),
        required=False,
    )

    write_permission(startitem='collective.conferences.ModifyTalktime')
    startitem = schema.Datetime(
        title=_(safe_unicode('Startdate')),
        description=_(safe_unicode('Start date')),
        defaultFactory=startDefaultValue,
        required=False,
    )

    write_permission(enditem='collective.conferences.ModifyTalktime')
    enditem = schema.Datetime(
        title=_(safe_unicode('Enddate')),
        description=_(safe_unicode('End date')),
        defaultFactory=endDefaultValue,
        required=False,
    )

    model.fieldset('slides',
                   label=_(safe_unicode('Slides')),
                   fields=['slidefileextension',
                           'slides',
                           'slides2',
                           'slides3',
                           'slides4',
                           ],
                   )

    model.fieldset('files',
                   label=_(safe_unicode('Files / Material')),
                   fields=['materialfileextension',
                           'material',
                           ],
                   )

    model.fieldset('video',
                   label=_(safe_unicode('Video')),
                   fields=['videofileextension',
                           'video'],
                   )

    directives.mode(slidefileextension='display')
    slidefileextension = schema.TextLine(
        title=_(safe_unicode(
            'The following file extensions are allowed for the upload of '
            'slides of conference workshop as well as for linked slides '
            '(upper case and lower case and mix of both):')),
        defaultFactory=allowedconferenceworkshopslideextensions,
    )

    slides = NamedBlobFile(
        title=_(safe_unicode('Presentation slides')),
        description=_(safe_unicode(
            'If you used slides during your workshop, please upload your '
            'slides shortly after you have given your workshop.')),
        constraint=validateworshopslidefileextension,
        required=False,
    )

    slides2 = NamedBlobFile(
        title=_(safe_unicode(
            'Presentation Slides In Further File Format')),
        description=_(safe_unicode(
            'If you used slides during your workshop, please upload your '
            'slides shortly after you have given your workshop.')),
        constraint=validateworshopslidefileextension,
        required=False,
    )

    slides3 = schema.URI(
        title=_(safe_unicode('Link To The Presentation Slides')),
        constraint=validatelinkedworkshopslidefileextension,
        required=False,
    )

    slides4 = schema.URI(
        title=_(safe_unicode(
            'Link To The Presentation Slides In Further File Format')),
        constraint=validatelinkedworkshopslidefileextension,
        required=False,
    )

    directives.mode(materialfileextension='display')
    materialfileextension = schema.TextLine(
        title=_(safe_unicode(
            'The following file extensions are allowed for workshop '
            'material uploads (upper case and lower case and mix of both):')),
        defaultFactory=allowedconferenceworkshopmaterialextensions,
    )

    material = NamedBlobFile(
        title=_(safe_unicode('Workshop slides / material')),
        description=_(safe_unicode(
            'Please upload your workshop presentation or material about the content of the workshop '
            'in front or short after you have given the workshop.')),
        constraint=validateworkshopmaterialfileextension,
        required=False,
    )

    directives.mode(videofileextension='display')
    videofileextension = schema.TextLine(
        title=_(safe_unicode(
            'The following file extensions are allowed for conference '
            'video uploads (upper case and lower case and mix of both):')),
        defaultFactory=allowedconferencevideoextensions,
    )

    video = schema.URI(
        title=_(safe_unicode('Link to the Video of the talk')),
        constraint=validatevideofileextension,
        required=False,
    )

    read_permission(reviewNotes='cmf.ReviewPortalContent')
    write_permission(reviewNotes='cmf.ReviewPortalContent')
    reviewNotes = schema.Text(
        title=_(safe_unicode('Review notes')),
        required=False,
    )

    @invariant
    def validateLicensechoosen(data):
        if not data.license:
            raise ChooseLicense(
                _(safe_unicode('Please choose a license for your talk.'),
                  ),
            )

    @invariant
    def trackpositionset(value):
        if value.conferencetrack and not value.positionintrack:
            raise Invalid(_(safe_unicode('You need to choose a position in the track. Please '
                                         "add this position to the field 'Position in Track'.")))

    @invariant
    def validatecfptopicchoosen(data):
        if not data.call_for_paper_topic:
            raise ChooseCfpTopic(
                _(safe_unicode('Please choose a call for paper topic for your workshop.'),
                  ),
            )

    @invariant
    def validateplanedlengthchoosen(data):
        if not data.planedworkshoplength:
            raise ChoosePlanedLength(
                _(safe_unicode('Please choose a planed length for your workshop.'),
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

        try:
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

        except Exception:
            api.portal.send_email(
                recipient=contactaddress,
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


def notifyAboutWorkflowChange(self, event):
    state = api.content.get_state(self)
    if api.portal.get_registry_record(
            'plone.email_from_address') is not None:
        contactaddress = api.portal.get_registry_record(
            'plone.email_from_address')
        current_user = api.user.get_current()
        try:
            api.portal.send_email(
                recipient=current_user.getProperty('email'),
                sender=contactaddress,
                subject=(safe_unicode('Your Workshop Proposal {0}')).format(self.title),
                body=(safe_unicode(
                    'The status of your proposed workshop changed. '
                    'The new status is {0}')).format(state),
            )

        except Exception:
            api.portal.send_email(
                recipient=contactaddress,
                sender=contactaddress,
                subject=(safe_unicode('Your Workshop Proposal {0}')).format(self.title),
                body=(safe_unicode(
                    'The status of your proposed workshop changed. '
                    'The new status is {0}')).format(state),
            )


class ValidateWorkshopUniqueness(validator.SimpleFieldValidator):
    # Validate site-wide uniqueness of project titles.

    def validate(self, value):
        # Perform the standard validation first

        super(ValidateWorkshopUniqueness, self).validate(value)
        if value is not None:
            catalog = api.portal.get_tool(name='portal_catalog')
            results = catalog({'Title': quote_chars(value),
                               'portal_type': ('collective.conferences.workshop',
                                               'collective.conferences.talk')})
            contextUUID = api.content.get_uuid(self.context)
            for result in results:
                if result.UID != contextUUID:
                    raise Invalid(_(u'The talk title is already in use.'))


validator.WidgetValidatorDiscriminators(
    ValidateWorkshopUniqueness,
    field=IWorkshop['title'],
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
