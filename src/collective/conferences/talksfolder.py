# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.supermodel import model
from Products.Five import BrowserView
from zope import schema


class ITalkfolder(model.Schema):

    title=schema.TextLine(
        title=_(u'Name Of The Folder For Talks'),
    )

    description=scheam.Text(
        title=_(u'Talk Folder Description'),
        required=False,
    )


class TalkfolderView(BrowserView):

    pass