# -*- coding: utf-8 -*-
from collective.conferences import _
from plone import api
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
        default=_(safe_unicode('Talks / Workshops')),
    )

    description = schema.Text(
        title=_(safe_unicode('Summary For Talks And Workshops')),
    )


class TWFolderView(BrowserView):
    def allconferencetalks(self):
        current_path = '/'.join(self.context.getPhysicalPath())
        res = api.content.find(
            portal_type=('collective.conferences.talk'),
            path=current_path,
            sort_on='Date',
            sort_order='reverse')
        return [r.getObject() for r in res]

    def allconferenceworkshops(self):
        current_path = '/'.join(self.context.getPhysicalPath())
        res = api.content.find(
            portal_type=('collective.conferences.workshop'),
            path=current_path,
            sort_on='Date',
            sort_order='reverse')
        return [r.getObject() for r in res]
