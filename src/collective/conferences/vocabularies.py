# -*- coding: utf-8 -*-
from plone import api
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory

@provider(IVocabularyFactory)
def BreakLengthVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveconf.break_length')
    return safe_simplevocabulary_from_values(values)