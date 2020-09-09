# -*- coding: utf-8 -*-
from collective.conferences import _
from collective.conferences.common import validateEmail
from collective.conferences.common import yesnochoice
from plone import api
from plone.autoform import directives
from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.supermodel import model
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema


class IAttendee(model.Schema):
    """A conference attendee. Attendees can be added anywhere.
    """

    title = schema.TextLine(
        title=_(safe_unicode('Firstname Lastname')),
    )

    street = schema.TextLine(
        title=_(safe_unicode('Street')),
        description=_(safe_unicode('This data is mandatory and required for our internal procedures')),
        required=True,
    )

    city = schema.TextLine(
        title=_(safe_unicode('City')),
        description=_(safe_unicode('This data is mandatory and required for our internal procedures')),
        required=True,
    )

    postalcode = schema.TextLine(
        title=_(safe_unicode('Postal Code')),
        description=_(safe_unicode('This data is mandatory and required for our internal procedures')),
        required=True,
    )

    country = schema.TextLine(
        title=_(safe_unicode('Country')),
        description=_(safe_unicode('This data is mandatory and required for our internal procedures')),
        required=True,
    )

    email = schema.TextLine(
        title=_(safe_unicode('E-Mail')),
        description=_(safe_unicode('We need this mandatory data to get in contact with you, if we have any questions')),
        constraint=validateEmail,
        required=True,
    )

    organisation = schema.TextLine(
        title=_(safe_unicode('Organisation')),
        required=False,
    )

    registrationpayed = schema.Choice(
        title=_(safe_unicode('Payment of the Registration Fee')),
        description=_(safe_unicode('Have you already paid the registration fee?')),
        vocabulary=yesnochoice,
        required=True,
    )

    directives.widget(paymentway=RadioFieldWidget)
    paymentway = schema.List(
        title=_(safe_unicode('Way of Registration Fee Payment')),
        description=_(safe_unicode(
            'If you already payed the registration fee, please tell us, which way you used to transfer the money.')),
        value_type=schema.Choice(source='PaymentOptions'),
        required=False,
    )

    usedbank = schema.TextLine(
        title=_(safe_unicode('Used Bank Account')),
        description=_(safe_unicode(
            'If you transfered the Registration Fee via a bank account, please tell us the name and branch '
            'of the bank you used. We need this information to identify your payment more quickly.')),
        required=False,
    )


class AttendeeAddForm(add.DefaultAddForm):
    portal_type = 'collective.conferences.attendee'

    def updateWidgets(self):
        super(AttendeeAddForm, self).updateWidgets()
        if api.portal.get_registry_record('collectiveconference.conferencefee') == 0:
            self.widgets['registrationpayed'].mode = 'hidden'
            self.widgets['paymentway'].mode = 'hidden'
            self.widgets['usedbank'].mode = 'hidden'


class AttendeeAddView(add.DefaultAddView):
    form = AttendeeAddForm


class AttendeeEditForm(edit.DefaultEditForm):

    def updateWidgets(self):
        super(AttendeeEditForm, self).updateWidgets()
        if api.portal.get_registry_record('collectiveconference.conferencefee') == 0:
            self.widgets['registrationpayed'].mode = 'hidden'
            self.widgets['paymentway'].mode = 'hidden'
            self.widgets['usedbank'].mode = 'hidden'


class AttendeeView(BrowserView):
    pass
