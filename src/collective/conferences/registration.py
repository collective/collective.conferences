# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.app.textfield import RichText
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from zope import schema


class IRegistration(model.Schema):
    title = schema.TextLine(
        title=_(safe_unicode('Title of the Registration Page')),
    )

    description = schema.Text(
        title=_(safe_unicode('Registration Description')),
        required=False,
    )

    primary('moreinformation')
    moreinformation = RichText(
        title=_(safe_unicode('Information About The Registration Process')),
        required=False,
    )


class RegistrationView(BrowserView):
    pass
