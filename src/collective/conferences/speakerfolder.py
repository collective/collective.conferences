# -*- coding: utf-8 -*-
from collective.conferences import _
from plone import api
from plone.supermodel import model
from Products.Five import BrowserView
from zope import schema


class ISpeakerfolder(model.Schema):
    """A speaker folder. The speaker of the conference are created in the folder.
    """

    title = schema.TextLine(
        title=_(u'Name of the speaker folder'),
    )

    description = schema.Text(
        title=_(u'speakerfolder description'),
        required=False,
    )


class SpeakerfolderView(BrowserView):

    def canRequestReview(self):
        return api.user.has_permission('cmf.RequestReview', obj=self.context)