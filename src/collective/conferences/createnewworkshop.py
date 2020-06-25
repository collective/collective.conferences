# -*- coding: utf-8 -*-
import logging

from Acquisition import aq_inner
from collective.conferences import _
from plone import api
from plone.app.textfield import RichText
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform.form import AutoExtensibleForm
from plone.formwidget.recaptcha.widget import ReCaptchaFieldWidget
from plone.z3cform.layout import wrap_form
from Products.CMFPlone.utils import safe_unicode
from z3c.form import button, field, form
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import RelationChoice, RelationList
from zope import interface, schema
from zope.component import adapter, getMultiAdapter
from zope.interface import directlyProvides, implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

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

    workshoptitle=schema.TextLine(
        title=_(u'The Title Of Your Workshop'),
        description=_(u'Fill in the title of your proposed conference workshop'),
    )

    workshopdescription = schema.Text(
        title=_(u"Workshop summary"),
    )

    workshopdetails = RichText(
            title=_(u"Workshop details"),
            required=True
        )

    speaker = RelationList(
        title=_(u'Workshop Leader'),
        default=[],
        value_type=RelationChoice(vocabulary='ConferenceSpeaker'),
        required=False,
        missing_value=[],
    )

    cfp_topic = schema.List(
        title=_(u"Choose the topic for your workshop"),
        value_type=schema.Choice(source=vocabCfPTopics),
        required=True,
    )

    wtalklength = schema.List(
        title=_(u"Planed Length"),
        description=_(u"Give an estimation about the time you'd plan for your workshop."),
        value_type=schema.Choice(source="WorkshopLength"),
        required=True,
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

        portal=api.portal.get()
        obj=api.content.create(
            type='collective.conferences.workshop',
            title=data['workshoptitle'],
            description=data['workshopdescription'],
            details=data['workshopdetails'],
            call_for_paper_topic=data['cfp_topic'],
            planedworkshoplength=data['wtalklength'],
            container=portal['workshops'],
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
