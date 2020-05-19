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
