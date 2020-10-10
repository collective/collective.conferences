# -*- coding: utf-8 -*-
from collective.conferences import _
from plone import api
from plone.app.textfield import RichText
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class ITraining(model.Schema):
    """A conference workshop.
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
        value_type=schema.Choice(source='TrainingsLength'),
        required=True,
    )

    directives.widget(license=RadioFieldWidget)
    license = schema.List(
        title=_(safe_unicode('License Of Your Training')),
        description=_(safe_unicode('Choose a license for the training')),
        value_type=schema.Choice(source='ContentLicense'),
        required=True,
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

    messagetocommittee = schema.Text(
        title=_(safe_unicode('Messages to the Program Committee')),
        description=_(safe_unicode(
            'You can give some information to the committee here, e.g. about days you are (not) '
            'available to give the workshop')),
        required=False,
    )


class TrainingView(BrowserView):

    def canRequestReview(self):
        return api.user.has_permission('cmf.RequestReview', obj=self.context)
