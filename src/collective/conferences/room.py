# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.Five import BrowserView
from zope import schema


class IRoom(model.Schema):
    """A conference room.
    """
    
    title = schema.TextLine(
            title=_(u"Name of the Room"),
        )


    description = schema.Text(
            title=_(u"A description of the room and its location"),
        )

    
    picture = NamedBlobImage(
            title=_(u"A picture of the room"),
            description=_(u"Please upload an image"),
            required=False,
        )
    
    primary ('details')
    details = RichText(
             title=_(u"A full description of the room, it's location and the way to get there"),
             required=True,                          
        )
    
    capacity = schema.Int(
             title=_(u"Capacity of the room"),
             description=_(u"Please fill in the maximum number of attendees"),
             required=False,
        )


class RoomView(BrowserView):
    pass
