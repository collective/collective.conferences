# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.supermodel import model
from zope import schema
from plone.app.textfield import RichText
from plone.supermodel.directives import primary


class IConference(model.Schema):

    title = schema.TextLine(
        title=_(u"Conference Title"),
    )

    description = schema.Text(
        title=_(u"Conference summary"),
        required= False
    )

    primary('details')
    details = RichText(
        title=_(u"Details"),
        description=_(u"Write information about the conference"),
        required=False,
    )


    break_length = schema.List(
        title=_(u"Length Of Conference Breaks"),
        description=_(u"Fill in the time slots for conference breaks in minutes. Use a new line for every "
                      u"value / talk length. Write only the numbers without the addition 'minutes'."),
        value_type=schema.TextLine(),
        required=True,
    )

    talk_length = schema.List(
        title=_(u"Length Of Talks"),
        description=_(u"Fill in the time slots for conference talks in minutes. Use a new line for every "
                      u"value / talk length. Write only the numbers without the addition 'minutes'."),
        value_type=schema.TextLine(),
        required=True,
    )

    workshop_length = schema.List(
        title=_(u"Length Of Workshops"),
        description=_(u"Fill in the time slots for workshops at the conference in minutes. Use a new line for every "
                      u"value / workshop length. Write only the numbers without the addition 'minutes'."),
        value_type=schema.TextLine(),
        required=True,
    )
