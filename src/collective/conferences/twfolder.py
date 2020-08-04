# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.autoform import directives
from plone.supermodel import model
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from zope import schema


class ITWFolder(model.Schema):
    directives.mode(title='hidden')
    title = schema.TextLine(
        title=_(safe_unicode('Title')),
        description=_(safe_unicode('Talk workshop folder title')),
        default=_(safe_unicode('Talks Workshops')),
    )

    description = schema.Text(
        title=_(safe_unicode('Workshop summary')),
    )


class TWFolderView(BrowserView):
    pass
