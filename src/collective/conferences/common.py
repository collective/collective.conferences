# -*- coding: utf-8 -*-
from collective.conferences import _
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import datetime


yesnochoice = SimpleVocabulary(
    [SimpleTerm(value=0, title=_(u'No')),
     SimpleTerm(value=1, title=_(u'Yes'))],
)


def startDefaultValue():
    return datetime.datetime.today() + datetime.timedelta(14)


def endDefaultValue():
    return datetime.datetime.today() + datetime.timedelta(17)
