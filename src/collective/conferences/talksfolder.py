# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.autoform import directives
from plone.supermodel import model
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from zope import schema


class ITalksfolder(model.Schema):
    directives.mode(title='hidden')
    title = schema.TextLine(
        title=_(safe_unicode('Name Of The Folder For Talks')),
        default=_(safe_unicode('Talks')),
    )

    description = schema.Text(
        title=_(safe_unicode('Talk Folder Description')),
        required=False,
    )


class TalksfolderView(BrowserView):
    pass
