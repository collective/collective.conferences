# -*- coding: utf-8 -*-
from collective.conferences import _
from zope import schema
from plone.supermodel import model
from plone.app.textfield import RichText
from plone.supermodel.directives import primary
from Products.Five import BrowserView
from plone import api

from zope.component import createObject
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent
from zope.filerepresentation.interfaces import IFileFactory




from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName



class ICallforpaper(model.Schema):
    """A call for paper for a conferences.
    A call for paper can contain incomming talks.
    """
    
    
    title = schema.TextLine(
            title=_(u"Call for paper title"),
        )

    description = schema.Text(
        title=_(u"Call for paper summary"),
        required=False,
        )
    
    
    primary('details')
    details = RichText(
            title=_(u"Details"),
            description=_(u"Details about the program"),
            required=True,
        )
        
    cfp_topics = schema.List(title=_(u"Topics for the Call for Papers"),
           default=['Development',
                    'Documentation',
                    'Project-Administration'],
           value_type=schema.TextLine()
        )

# Views

class CallforpaperView(BrowserView):

    def talks(self):
        """Return a catalog search result of talks to show
        """

        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')

        return catalog(object_provides=ITalk.__identifier__,
                       path='/'.join(context.getPhysicalPath()),
                       sort_order='sortable_title')


# File representation

# class CallforpaperFileFactory(grok.Adapter):
#    """Custom file factory for programs, which always creates a Track.
#    """

#    grok.implements(IFileFactory)
#    grok.context(ICallforpaper)

#    def __call__(self, name, contentType, data):
#        talk = createObject('collective.conferences.talk')
#        notify(ObjectCreatedEvent(talk))
#        return talk
