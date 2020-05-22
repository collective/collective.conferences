# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.supermodel import model
from Products.Five import BrowserView
from zope import schema


class ITalksfolder(model.Schema):

    title=schema.TextLine(
        title=_(u'Name Of The Folder For Talks'),
    )

    description=schema.Text(
        title=_(u'Talk Folder Description'),
        required=False,
    )


class TalksfolderView(BrowserView):

    pass