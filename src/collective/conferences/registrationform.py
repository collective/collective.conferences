# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.conferences import _
from collective.conferences.common import validateEmail
from collective.conferences.common import yesnochoice
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.formwidget.recaptcha.widget import ReCaptchaFieldWidget
from Products.CMFPlone.utils import safe_unicode
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.browser.radio import RadioFieldWidget
from zope import interface
from zope import schema
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer

import logging


logger = logging.getLogger(__name__)


class IReCaptchaForm(interface.Interface):
    captcha = schema.TextLine(
        title=safe_unicode('ReCaptcha'),
        description=safe_unicode(''),
        required=False,
    )


class ReCaptcha(object):
    captcha = safe_unicode('')

    def __init__(self, context):
        self.context = context


class RegistrationMailSchema(interface.Interface):
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
        required=False,
    )

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


@implementer(RegistrationMailSchema)
@adapter(interface.Interface)
class RegistrationAdapter(object):

    def __init__(self, context):
        self.title = None
        self.street = None
        self.city = None
        self.postalcode = None
        self.country = None
        self.email = None
        self.organisation = None
        self.registrationpayed = None
        self.paymentway = None
        self.usedbank = None


class RegistrationForm(AutoExtensibleForm, form.Form):
    schema = RegistrationMailSchema
    form_name = 'registrationmail_form'

    label = _(safe_unicode('Mail To The Conference Organizer'))
    description = _(safe_unicode('Register for the conference.'))

    fields = field.Fields(RegistrationMailSchema, IReCaptchaForm)
    fields['captcha'].widgetFactory = ReCaptchaFieldWidget
    fields['paymentway'].widgetFactory = RadioFieldWidget

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)
        if api.portal.get_registry_record('collectiveconference.conferencefee') == 0:
            RegistrationForm.fields['registrationpayed'].mode = 'hidden'
            RegistrationForm.fields['paymentway'].mode = 'hidden'
            RegistrationForm.fields['usedbank'].mode = 'hidden'
        super(RegistrationForm, self).updateWidgets()

        # call the base class version - this is very important!
        super(RegistrationForm, self).update()
        if api.portal.get_registry_record('collectiveconference.conferencefee') == 0:
            RegistrationForm.fields['registrationpayed'].mode = 'hidden'
            RegistrationForm.fields['paymentway'].mode = 'hidden'
            RegistrationForm.fields['usedbank'].mode = 'hidden'
        super(RegistrationForm, self).updateWidgets()

    @button.buttonAndHandler(_(u'Send Email'))
    def handleApply(self, action):
        data, errors = self.extractData()
        captcha = getMultiAdapter(
            (aq_inner(self.context), self.request),
            name='recaptcha',
        )

        if errors:
            self.status = self.formErrorsMessage
            return

        elif captcha.verify():
            logger.info('ReCaptcha validation passed.')
        else:
            logger.info(
                'Please validate the recaptcha field before sending the form.')
            api.portal.show_message(
                message=_(
                    safe_unicode('Please validate the recaptcha field before '
                                 'sending the form.')),
                request=self.request,
                type='error')
            return

        if api.portal.get_registry_record('plone.email_from_address') \
                is not None:
            contactaddress = api.portal.get_registry_record(
                'plone.email_from_address')

        if (data['registrationpayed']) == 0:
            rgp = 'No'
        else:
            rgp = 'Yes'

        if not (data['paymentway']):
            pmw = None
        else:
            pmw = (data['paymentway'])[0]

        api.portal.send_email(
            recipient=contactaddress,
            sender=(safe_unicode('{0} <{1}>')).format(
                data['title'],
                data['email']),
            subject=(safe_unicode('Registration For The Conference')),
            body=((safe_unicode('The following user registered for the conference:\n'
                                'name: {0}\n'
                                'street: {1}\n'
                                'city: {2}\n'
                                'country: {3}\n'
                                'organization: {4}\n'
                                'Registration Fee Payed: {5}\n'
                                'Way of Payment: {6}\n'
                                'Used Bank: {7}')).
                  format(data['title'],
                         data['street'],
                         data['city'],
                         data['country'],
                         data['organisation'],
                         rgp,
                         pmw,
                         data['usedbank'])),
        )

        # Redirect back to the front page with a status message
        api.portal.show_message(
            message=_(safe_unicode('We send your message to the conference organizers.')),
            request=self.request,
            type='info')

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)

    @button.buttonAndHandler(_(safe_unicode('Cancel')))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
            """
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
