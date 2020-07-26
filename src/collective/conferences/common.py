# -*- coding: utf-8 -*-
from collective.conferences import _
from Products.CMFPlone.utils import safe_unicode
from zope.interface import Invalid
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import datetime
import re


yesnochoice = SimpleVocabulary(
    [SimpleTerm(value=0, title=_(u'No')),
     SimpleTerm(value=1, title=_(u'Yes'))],
)


def startDefaultValue():
    return datetime.datetime.today() + datetime.timedelta(14)


def endDefaultValue():
    return datetime.datetime.today() + datetime.timedelta(17)


checkEmail = re.compile(
    r'[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}').match


def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(
            safe_unicode('Invalid email address')))
    return True
