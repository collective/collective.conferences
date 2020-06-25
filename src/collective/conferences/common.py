# -*- coding: utf-8 -*-
from collective.conferences import _
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

yesnochoice = SimpleVocabulary(
    [SimpleTerm(value=0, title=_(u'No')),
     SimpleTerm(value=1, title=_(u'Yes'))],
)
