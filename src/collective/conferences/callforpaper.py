# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.app.textfield import RichText
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from zope import schema


class ICallforpaper(model.Schema):
    """A call for paper for a conferences.
    A call for paper can contain incomming talks.
    """
    title = schema.TextLine(
        title=_(safe_unicode('Call for paper title')),
    )

    description = schema.Text(
        title=_(safe_unicode('Call for paper summary')),
        required=False,
    )

    primary('details')
    details = RichText(
        title=_(safe_unicode('Details')),
        description=_(safe_unicode('Details about the program')),
        required=True,
    )

    cfp_topics = schema.List(title=_(safe_unicode('Topics for the Call for Papers')),
                             description=_(
                                 safe_unicode('Fill in the topics for conference talks and workshops. '
                                              'Use a new line for every value / topic.')),
                             default=['Development',
                                      'Documentation',
                                      'Project-Administration'],
                             value_type=schema.TextLine(),
                             )


# Views

class CallforpaperView(BrowserView):
    pass
