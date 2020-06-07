# -*- coding: utf-8 -*-
from plone import api
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import implementer


@provider(IVocabularyFactory)
def BreakLengthVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveconf.break_length')
    return safe_simplevocabulary_from_values(values)

@provider(IVocabularyFactory)
def TalkLengthVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveconf.talk_length')
    return safe_simplevocabulary_from_values(values)

@provider(IVocabularyFactory)
def WorkshopLengthVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveconf.workshop_length')
    return safe_simplevocabulary_from_values(values)

@implementer(IVocabularyFactory)
class ConferenceSpeakerVocabulary(object):

    def __call__(self, context=None):
        terms = []
        # Use getObject since the DataConverter expects a real object.
        for brain in api.content.find(portal_type='collective.conferences.conferencespeaker', sort_on='sortable_title'):
            terms.append(SimpleTerm(
                value=brain.getObject(),
                token=brain.UID,
                title=u'{} ({})'.format(brain.Title, brain.getPath()),
            ))
        return SimpleVocabulary(terms)


ConferenceSpeakerVocabularyFactory = ConferenceSpeakerVocabulary()
