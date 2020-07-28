# -*- coding: utf-8 -*-
from collective.conferences import _
from plone import api
from plone.supermodel import model
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from zope import schema


class ISpeakerfolder(model.Schema):
    """A speaker folder. The speaker of the conference are created in the folder.
    """

    title = schema.TextLine(
        title=_(safe_unicode('Name of the speaker folder')),
    )

    description = schema.Text(
        title=_(safe_unicode('speakerfolder description')),
        required=False,
    )


class SpeakerfolderView(BrowserView):

    def canRequestReview(self):
        return api.user.has_permission('cmf.RequestReview', obj=self.context)
