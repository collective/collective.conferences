# -*- coding: utf-8 -*-
from collective.conferences import _
from collective.conferences.common import allowedconferencetrainingmaterialextensions
from collective.conferences.common import allowedconferencetrainingslideextensions
from collective.conferences.common import allowedconferencevideoextensions
from collective.conferences.common import endDefaultValue
from collective.conferences.common import startDefaultValue
from collective.conferences.common import validatelinkedtrainingslidefileextension
from collective.conferences.common import validatetrainingmaterialfileextension
from collective.conferences.common import validatetrainingslidefileextension
from collective.conferences.common import validatevideofileextension
from plone import api
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
        title=_(safe_unicode('Workshop details')),
        required=False,
    )

    speaker = RelationList(
        title=_(safe_unicode('Trainer')),
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


class TrainingView(BrowserView):

    def canRequestReview(self):
        return api.user.has_permission('cmf.RequestReview', obj=self.context)
