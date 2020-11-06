# -*- coding: utf-8 -*-
from collective.conferences import _
from collective.conferences.common import allowedconferencetrainingmaterialextensions
from collective.conferences.common import allowedconferencetrainingslideextensions
from collective.conferences.common import allowedconferencevideoextensions
from collective.conferences.common import endDefaultValue
from collective.conferences.common import quote_chars
from collective.conferences.common import startDefaultValue
from collective.conferences.common import validatelinkedtrainingslidefileextension
from collective.conferences.common import validatetrainingmaterialfileextension
from collective.conferences.common import validatetrainingslidefileextension
from collective.conferences.common import validatevideofileextension
from datetime import timedelta
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
from zope.interface import Invalid
from zope.interface import invariant

import transaction


class StartBeforeEnd(Invalid):
    __doc__ = _(safe_unicode('The start or end date is invalid'))


class ChooseLicense(Invalid):
    __doc__ = _(safe_unicode(
        'Please choose a license for your training.'))


class ChoosePlanedLength(Invalid):
    __doc__ = _(safe_unicode(
        'Please choose a planed length for your training.'))


class ITraining(model.Schema):
    """A conference training.
    """

    title = schema.TextLine(
        title=_(safe_unicode('Title')),
        description=_(safe_unicode('Training title')),
    )

    description = schema.Text(
        title=_(safe_unicode('Training Summary')),
    )

    primary('details')
    details = RichText(
        title=_(safe_unicode('Training Details')),
        required=False,
    )

    speaker = RelationList(
        title=_(safe_unicode('Instructor')),
        description=_(safe_unicode('Click with the mouse pointer into the field and choose the '
                                   'instructor(s) from the appearing list.')),
        default=[],
        value_type=RelationChoice(vocabulary='ConferenceSpeaker'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'speaker',
        SelectFieldWidget,
    )

    level = schema.Choice(
        title=_(safe_unicode('Level')),
        description=_(safe_unicode('Choose the level of the training.')),
        required=True,
        source='TrainingLevel',
    )

    audience = schema.Set(
        title=_(safe_unicode('Audience')),
        description=_(safe_unicode('Choose the audience of the training.')),
        required=True,
        value_type=schema.Choice(source='TrainingAudience'),
    )

    directives.widget(planedtraininglength=RadioFieldWidget)
    planedtraininglength = schema.List(
        title=_(safe_unicode('Planed Length')),
        description=_(safe_unicode(
            "Give an estimation about the time you'd plan for the training.")),
        value_type=schema.Choice(source='TrainingLength'),
        required=True,
    )

    directives.widget(license=RadioFieldWidget)
    license = schema.List(
        title=_(safe_unicode('License Of Your Training')),
        description=_(safe_unicode('Choose a license for the training')),
        value_type=schema.Choice(source='ContentLicense'),
        required=True,
    )

    messagetocommittee = schema.Text(
        title=_(safe_unicode('Messages to the Program Committee')),
        description=_(safe_unicode(
            'You can give some information to the committee here, e.g. about days you are (not) '
            'available to give the workshop')),
        required=False,
    )

    read_permission(traininglength='cmf.ReviewPortalContent')
    write_permission(traininglength='cmf.ReviewPortalContent')
    directives.widget(traininglength=RadioFieldWidget)
    traininglength = schema.List(
        title=_(safe_unicode('Training Length')),
        description=_(safe_unicode('Set a time frame for the training in minutes.')),
        value_type=schema.Choice(source='TrainingLength'),
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

    read_permission(room='cmf.ReviewPortalContent')
    write_permission(room='cmf.ReviewPortalContent')
    room = RelationList(
        title=_(safe_unicode('Room')),
        description=_(safe_unicode('Choose the room for the training')),
        default=[],
        value_type=RelationChoice(vocabulary='ConferenceRoom'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'room',
        RadioFieldWidget,
    )

    model.fieldset('slides',
                   label=_(safe_unicode('Slides')),
                   fields=['slidefileextension', 'slides', 'slides2', 'slides3', 'slides4'],
                   )

    model.fieldset('material',
                   label=_(safe_unicode('Material')),
                   fields=['materialfileextension',
                           'material'],
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
        defaultFactory=allowedconferencetrainingslideextensions,
    )

    slides = NamedBlobFile(
        title=_(safe_unicode('Presentation slides')),
        description=_(safe_unicode(
            'If you used slides during your workshop, please upload your '
            'slides shortly after you have given your workshop.')),
        constraint=validatetrainingslidefileextension,
        required=False,
    )

    slides2 = NamedBlobFile(
        title=_(safe_unicode(
            'Presentation Slides In Further File Format')),
        description=_(safe_unicode(
            'If you used slides during your workshop, please upload your '
            'slides shortly after you have given your workshop.')),
        constraint=validatetrainingslidefileextension,
        required=False,
    )

    slides3 = schema.URI(
        title=_(safe_unicode('Link To The Presentation Slides')),
        constraint=validatelinkedtrainingslidefileextension,
        required=False,
    )

    slides4 = schema.URI(
        title=_(safe_unicode(
            'Link To The Presentation Slides In Further File Format')),
        constraint=validatelinkedtrainingslidefileextension,
        required=False,
    )

    directives.mode(materialfileextension='display')
    materialfileextension = schema.TextLine(
        title=_(safe_unicode(
            'The following file extensions are allowed for workshop '
            'material uploads (upper case and lower case and mix of both):')),
        defaultFactory=allowedconferencetrainingmaterialextensions,
    )

    material = NamedBlobFile(
        title=_(safe_unicode('Workshop slides / material')),
        description=_(safe_unicode(
            'Please upload your workshop presentation or material about the content of the workshop '
            'in front or short after you have given the workshop.')),
        constraint=validatetrainingmaterialfileextension,
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

    @invariant
    def validateLicensechoosen(data):
        if not data.license:
            raise ChooseLicense(
                _(safe_unicode('Please choose a license for your talk.'),
                  ),
            )

    @invariant
    def validateplanedlengthchoosen(data):
        if not data.planedtraininglength:
            raise ChoosePlanedLength(
                _(safe_unicode('Please choose a planed length for your training.'),
                  ),
            )

    @invariant
    def validateStartEnd(data):
        if data.startitem is not None and data.enditem is not None:
            if data.startitem > data.enditem:
                raise StartBeforeEnd(_(
                    safe_unicode(
                        'The start date must be before the end date.')))


def settrainingend(self, event):
    if self.startitem:
        if self.traininglength:
            start = self.startitem
            delta = timedelta(minutes=int(self.traininglength[0]))
            self.enditem = start + delta
            transaction.commit()
        else:
            return
    else:
        return


def newtrainingadded(self, event):
    if api.portal.get_registry_record(
            'plone.email_from_address') is not None:
        contactaddress = api.portal.get_registry_record(
            'plone.email_from_address')
        current_user = api.user.get_current()
        level = self.level
        audience = self.audience
        length = self.planedtraininglength[0]
        details = self.details.output

        try:
            api.portal.send_email(
                recipient=current_user.getProperty('email'),
                sender=contactaddress,
                subject=safe_unicode('Your Training Proposal'),
                body=safe_unicode('You submitted a conference training:\n'
                                  'title: {0},\n'
                                  'summary: {1},\n'
                                  'details: {2},\n'
                                  'proposed length: {3} minutes\n'
                                  'level: {4}\n'
                                  'audience: {5}\n'
                                  'committee: {6}\n\n'
                                  'Best regards,\n'
                                  'The Conference Committee').format(
                    self.title, self.description, details,
                    length, level, audience, self.messagetocommittee),
            )

        except Exception:
            api.portal.send_email(
                recipient=contactaddress,
                sender=contactaddress,
                subject=safe_unicode('Your Training Proposal'),
                body=safe_unicode('You submitted a conference training:\n'
                                  'title: {0},\n'
                                  'summary: {1},\n'
                                  'details: {2},\n'
                                  'proposed length: {3} minutes\n'
                                  'level: {4}\n'
                                  'audience: {5}\n'
                                  'committee: {6}\n\n'
                                  'Best regards,\n'
                                  'The Conference Committee').format(
                    self.title, self.description, details,
                    length, level, audience, self.messagetocommittee),
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
                subject=(safe_unicode('Your Training Proposal {0}')).format(self.title),
                body=(safe_unicode(
                    'The status of your proposed training changed. '
                    'The new status is {0}')).format(state),
            )

        except Exception:
            api.portal.send_email(
                recipient=contactaddress,
                sender=contactaddress,
                subject=(safe_unicode('Your Training Proposal {0}')).format(self.title),
                body=(safe_unicode(
                    'The status of your proposed training changed. '
                    'The new status is {0}')).format(state),
            )


class ValidateTrainingUniqueness(validator.SimpleFieldValidator):
    # Validate site-wide uniqueness of training titles.

    def validate(self, value):
        # Perform the standard validation first

        super(ValidateTrainingUniqueness, self).validate(value)
        if value is not None:
            catalog = api.portal.get_tool(name='portal_catalog')
            results = catalog({'Title': quote_chars(value),
                               'object_provides':
                                   ITraining.__identifier__})
            contextUUID = api.content.get_uuid(self.context)
            for result in results:
                if result.UID != contextUUID:
                    raise Invalid(_(u'The training title is already in use.'))


validator.WidgetValidatorDiscriminators(
    ValidateTrainingUniqueness,
    field=ITraining['title'],
)


class TrainingView(BrowserView):

    def canRequestReview(self):
        return api.user.has_permission('cmf.RequestReview', obj=self.context)

    def trainingInstructors(self):
        results = []
        for rel in self.context.speaker:
            if rel.isBroken():
                # skip broken relations
                continue
            obj = rel.to_object
            if api.user.has_permission('View', obj=obj):
                results.append(obj)
        return IContentListing(results)

    def trainingRoom(self):
        results = []
        for rel in self.context.room:
            if rel.isBroken():
                # skip broken relations
                continue
            obj = rel.to_object
            if api.user.has_permission('View', obj=obj):
                results.append(obj)
        return IContentListing(results)

    def trainingAudience(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        audience = idx_data.get('trainingaudience')
        return (r for r in audience)
