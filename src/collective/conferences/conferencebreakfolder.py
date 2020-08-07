# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.supermodel import model
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from zope import schema


class IConferencebreakFolder(model.Schema):
    title = schema.TextLine(
        title=_(safe_unicode('Title')),
        description=_(safe_unicode('Conference Break Folder Title')),
    )

    description = schema.Text(
        title=_(safe_unicode('Conference Break Summary')),
    )


class ConferencebreakFolderView(BrowserView):
    pass
