# -*- coding: utf-8 -*-
from collective.conferences import _
from plone import api
from plone.supermodel import model
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from zope import schema


class ITrainingFolder(model.Schema):
    title = schema.TextLine(
        title=_(safe_unicode('Title')),
        description=_(safe_unicode('Trainings folder title')),
        default=_(safe_unicode('Trainings')),
    )

    description = schema.Text(
        title=_(safe_unicode('Summary For Trainings')),
    )


class TrainingFolderView(BrowserView):

    def allconferencetrainings(self):
        current_path = '/'.join(self.context.getPhysicalPath())
        res = api.content.find(
            portal_type=('collective.conferences.training'),
            path=current_path,
            sort_on='Date',
            sort_order='reverse')
        return [r.getObject() for r in res]
