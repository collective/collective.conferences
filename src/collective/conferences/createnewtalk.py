# -*- coding: utf-8 -*-
from collective.conferences import _
from plone import api
from zope import interface
from zope import schema
from plone.app.textfield import RichText
from zope.interface import implementer
from zope.component import adapter
from plone.autoform.form import AutoExtensibleForm
from z3c.form import form
from Products.CMFPlone.utils import safe_unicode
from plone.z3cform.layout import wrap_form
from plone.formwidget.recaptcha.widget import ReCaptchaFieldWidget
from z3c.form import field
from z3c.form import button
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import directlyProvides
from z3c.form.browser.radio import RadioFieldWidget
from plone.autoform import directives
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


def vocabTalkLength(context):
    catalog = api.portal.get_tool(name='portal_catalog')
    results = catalog.uniqueValuesFor('talklength')
    terms = []
    for value in results:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))

    return SimpleVocabulary(terms)

directlyProvides(vocabTalkLength, IContextSourceBinder)



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



class NewTalkSchema(interface.Interface):

    talktitle=schema.TextLine(
        title=_(u'The Title Of Your Talk'),
        description=_(u'Fill in the title of your proposed conference talk'),
    )

    talkdescription = schema.Text(
        title=_(u"Talk summary"),
    )

    talkdetails = RichText(
            title=_(u"Talk details"),
            required=True
        )

    cfp_topic = schema.List(
        title=_(u"Choose the topic for your talk"),
        value_type=schema.Choice(source=vocabCfPTopics),
        required=True,
    )

    ptalklength = schema.List(
        title=_(u"Planed Length"),
        description=_(u"Give an estimation about the time you'd plan for plan for your talk."),
        value_type=schema.Choice(source=vocabTalkLength),
        required=True,
    )



@implementer(NewTalkSchema)
@adapter(interface.Interface)
class NewTalkSchemaAdapter(object):

    def __init__(self, context):
        self.talktitle = None
        self.talkdescription = None
        self.talkdetails = None
        self.cfp_topic = None
        self.ptalklength = None

class NewTalkForm(AutoExtensibleForm, form.Form):
    schema = NewTalkSchema
    form_name = 'newtalkform'
    label = _(safe_unicode('Submit A Conference Talk'))
    description = _(safe_unicode('Submit a proposal for a conference talk.'))


    fields = field.Fields(NewTalkSchema, IReCaptchaForm)
    fields['captcha'].widgetFactory = ReCaptchaFieldWidget
    fields['cfp_topic'].widgetFactory = RadioFieldWidget
    fields['ptalklength'].widgetFactory = RadioFieldWidget

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)

        # call the base class version - this is very important!
        super(NewTalkForm, self).update()


    @button.buttonAndHandler(_(safe_unicode('Submit Your talk')))
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
            type='collective.conferences.talk',
            title=data['talktitle'],
            description=data['talkdescription'],
            details=data['talkdetails'],
            call_for_paper_topic=data['cfp_topic'],
            planedtalklength=data['ptalklength'],
            container=portal['talks'],
        )

        api.portal.show_message(
            message=_(safe_unicode('The talk has been submitted.')),
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


ReCaptchaForm = wrap_form(NewTalkForm)
