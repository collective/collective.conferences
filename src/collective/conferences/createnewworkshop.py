# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.conferences import _
from plone import api
from plone.app.textfield import RichText
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform.form import AutoExtensibleForm
from plone.formwidget.recaptcha.widget import ReCaptchaFieldWidget
from plone.z3cform.layout import wrap_form
from Products.CMFPlone.utils import safe_unicode
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import interface
from zope import schema
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import directlyProvides
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import logging


logger = logging.getLogger(__name__)


def vocabCfPTopics(context):
    # For add forms
    catalog = api.portal.get_tool(name='portal_catalog')
    results = catalog.uniqueValuesFor('callforpaper_topics')
    terms = []
    for value in results:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))

    return SimpleVocabulary(terms)


directlyProvides(vocabCfPTopics, IContextSourceBinder)


class ChooseLicense(Invalid):
    __doc__ = _(safe_unicode(
        'Please choose a license for your talk.'))


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


class NewWorkshopSchema(interface.Interface):
    workshoptitle = schema.TextLine(
        title=_(u'The Title Of Your Workshop'),
        description=_(u'Fill in the title of your proposed conference workshop'),
    )

    workshopdescription = schema.Text(
        title=_(u'Workshop summary'),
    )

    workshopdetails = RichText(
        title=_(u'Workshop details'),
        required=True,
    )

    speaker = RelationList(
        title=_(u'Workshop Leader'),
        default=[],
        value_type=RelationChoice(vocabulary='ConferenceSpeaker'),
        required=False,
        missing_value=[],
    )

    cfp_topic = schema.List(
        title=_(u'Choose the topic for your workshop'),
        value_type=schema.Choice(source=vocabCfPTopics),
        required=True,
    )

    wtalklength = schema.List(
        title=_(u'Planed Length'),
        description=_(u"Give an estimation about the time you'd plan for your workshop."),
        value_type=schema.Choice(source='WorkshopLength'),
        required=True,
    )

    license = schema.List(
        title=_(u'License Of Your Talk'),
        description=_(u'Choose a license for your talk'),
        value_type=schema.Choice(source='ContentLicense'),
        required=True,
    )

    messagetocommittee = schema.Text(
        title=_(u'Messages to the Program Committee'),
        description=_(
            u'You can give some information to the committee here, e.g. about days you are (not) available '
            u'to give the workshop'),
        required=False,
    )

    @invariant
    def validateLicensechoosen(data):
        if not data.license:
            raise ChooseLicense(
                _(safe_unicode('Please choose a license for your talk.'),
                  ),
            )


@implementer(NewWorkshopSchema)
@adapter(interface.Interface)
class NewWorkshopSchemaAdapter(object):

    def __init__(self, context):
        self.workshoptitle = None
        self.workshopdescription = None
        self.workshopdetails = None
        self.speaker = None
        self.cfp_topic = None
        self.wtalklength = None
        self.messagetocommittee = None


class NewWorkshopForm(AutoExtensibleForm, form.Form):
    schema = NewWorkshopSchema
    form_name = 'newworkshopform'
    label = _(safe_unicode('Submit A Conference Workshop'))
    description = _(safe_unicode('Submit a proposal for a conference workshop.'))

    fields = field.Fields(NewWorkshopSchema, IReCaptchaForm)
    fields['captcha'].widgetFactory = ReCaptchaFieldWidget
    fields['cfp_topic'].widgetFactory = RadioFieldWidget
    fields['wtalklength'].widgetFactory = RadioFieldWidget
    fields['speaker'].widgetFactory = SelectFieldWidget
    fields['license'].widgetFactory = RadioFieldWidget

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)

        # call the base class version - this is very important!
        super(NewWorkshopForm, self).update()

    @button.buttonAndHandler(_(safe_unicode('Submit Your Workshop')))
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
                'Please validate the recaptcha field before sending the form.',
            )
            api.portal.show_message(
                message=_(
                    safe_unicode('Please validate the recaptcha field '
                                 'before sending the form.')),
                request=self.request,
                type='error')
            return

        portal = api.portal.get()
        api.content.create(
            type='collective.conferences.workshop',
            title=data['workshoptitle'],
            description=data['workshopdescription'],
            details=data['workshopdetails'],
            call_for_paper_topic=data['cfp_topic'],
            planedworkshoplength=data['wtalklength'],
            messagetocommittee=data['messagetocommittee'],
            container=portal['workshops'],
        )

        if api.portal.get_registry_record(
                'plone.email_from_address') is not None:
            contactaddress = api.portal.get_registry_record(
                'plone.email_from_address')
            current_user = api.user.get_current()
            length = (data['wtalklength'])[0]
            cfp = (data['cfp_topic'])[0]
            details = (data['workshopdetails']).output

            api.portal.send_email(
                recipient=current_user.getProperty('email'),
                sender=contactaddress,
                subject=safe_unicode('Your Workshop Proposal'),
                body=safe_unicode('You submitted a conference workshop:\n'
                                  'title: {0},\nsummary: {1},\ndetails: {2},\n'
                                  'proposed length: {3} minutes\nfor the call for papers '
                                  'topic: {4}\nwith the following message to the conference '
                                  'committee: {5}').format(
                    data['workshoptitle'], data['workshopdescription'], details,
                    length, cfp, data['messagetocommittee']),
            )

        api.portal.show_message(
            message=_(safe_unicode('The workshop has been submitted.')),
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


ReCaptchaForm = wrap_form(NewWorkshopForm)
