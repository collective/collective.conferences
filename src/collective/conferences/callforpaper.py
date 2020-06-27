# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.app.textfield import RichText
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.Five import BrowserView
from zope import schema


class ICallforpaper(model.Schema):
    """A call for paper for a conferences.
    A call for paper can contain incomming talks.
    """
    title = schema.TextLine(
        title=_(u'Call for paper title'),
    )

    description = schema.Text(
        title=_(u'Call for paper summary'),
        required=False,
    )

    primary('details')
    details = RichText(
        title=_(u'Details'),
        description=_(u'Details about the program'),
        required=True,
    )

    cfp_topics = schema.List(title=_(u'Topics for the Call for Papers'),
                             default=['Development',
                                      'Documentation',
                                      'Project-Administration'],
                             value_type=schema.TextLine(),
                             )


# Views

class CallforpaperView(BrowserView):
    pass
