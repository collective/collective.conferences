# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.app.textfield import RichText
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from zope import schema


class IConference(model.Schema):
    title = schema.TextLine(
        title=_(safe_unicode('Conference Title')),
    )

    description = schema.Text(
        title=_(safe_unicode('Conference summary')),
        required=False,
    )

    primary('details')
    details = RichText(
        title=_(safe_unicode('Details')),
        description=_(safe_unicode('Write information about the conference')),
        required=False,
    )


class ConferenceView(BrowserView):
    pass
