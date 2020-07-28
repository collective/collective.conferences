# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from zope import schema


class IRoom(model.Schema):
    """A conference room.
    """

    title = schema.TextLine(
        title=_(safe_unicode('Name of the Room')),
    )

    description = schema.Text(
        title=_(safe_unicode('A description of the room and its location')),
    )

    picture = NamedBlobImage(
        title=_(safe_unicode('A picture of the room')),
        description=_(safe_unicode('Please upload an image')),
        required=False,
    )

    primary('details')
    details = RichText(
        title=_(safe_unicode(
            "A full description of the room, it's location and the way to get there")),
        required=True,
    )

    capacity = schema.Int(
        title=_(safe_unicode('Capacity of the room')),
        description=_(safe_unicode('Please fill in the maximum number of attendees')),
        required=False,
    )


class RoomView(BrowserView):
    pass
