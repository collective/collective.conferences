# -*- coding: utf-8 -*-
from plone import api
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from Products.CMFPlone.utils import safe_unicode
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def BreakLengthVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveconference.break_length')
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def TalkLengthVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveconference.talk_length')
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def WorkshopLengthVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveconference.workshop_length')
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def TrainingLengthVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveconference.training_length')
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def TraningLevelVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveconference.traininglevel')
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def TrainingAudienceVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveconference.trainingsaudience')
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def LicenseVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveconference.license')
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def PaymentOptionsVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveconference.paymentoptions')
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
                title=safe_unicode('{0} ({1})').format(brain.Title, brain.getPath()),
            ))
        return SimpleVocabulary(terms)


ConferenceSpeakerVocabularyFactory = ConferenceSpeakerVocabulary()


@implementer(IVocabularyFactory)
class ConferenceRoomVocabulary(object):

    def __call__(self, context=None):
        terms = []
        # Use getObject since the DataConverter expects a real object.
        for brain in api.content.find(portal_type='collective.conferences.room', sort_on='sortable_title'):
            terms.append(SimpleTerm(
                value=brain.getObject(),
                token=brain.UID,
                title=safe_unicode('{0} ({1})').format(brain.Title, brain.getPath()),
            ))
        return SimpleVocabulary(terms)


ConferenceRoomVocabularyFactory = ConferenceRoomVocabulary()


@implementer(IVocabularyFactory)
class ConferenceTrackVocabulary(object):

    def __call__(self, context=None):
        terms = []
        # Use getObject since the DataConverter expects a real object.
        for brain in api.content.find(portal_type='collective.conferences.track', sort_on='sortable_title'):
            terms.append(SimpleTerm(
                value=brain.getObject(),
                token=brain.UID,
                title=safe_unicode('{0} ({1})').format(brain.Title, brain.getPath()),
            ))
        return SimpleVocabulary(terms)


ConferenceTrackVocabularyFactory = ConferenceTrackVocabulary()
