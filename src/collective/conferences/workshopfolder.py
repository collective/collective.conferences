# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.supermodel import model
from Products.Five import BrowserView
from zope import schema

class IWorkshopfolder(model.Schema):

    title=schema.TextLine(
        title=_(u'Name Of The Workshopfolder'),
    )

    description=schema.Text(
        title=_(u'Workshop Folder Description'),
        required=False,
    )


class WorkshopfolderView(BrowserView):

    pass