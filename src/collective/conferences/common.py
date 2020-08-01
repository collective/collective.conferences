# -*- coding: utf-8 -*-
from collective.conferences import _
from plone import api
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


def allowedconferenceimageextensions():
    return api.portal.get_registry_record('collectiveconference.allowed_conferenceimageextension').replace('|', ', ')


def allowedconferenceworkshopmaterialextensions():
    return api.portal.get_registry_record('collectiveconference.allowed_workshop_material_extension').replace('|', ', ')


def validateimagefileextension(value):
    result = str(api.portal.get_registry_record('collectiveconference.allowed_conferenceimageextension'))
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(safe_unicode(
            'You could only upload files with an allowed file extension. '
            'Please try again to upload a file with the correct file'
            'extension.'))
    return True


def validateworkshopmaterialfileextension(value):
    result = str(api.portal.get_registry_record('collectiveconference.allowed_workshop_material_extension'))
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(safe_unicode(
            'You could only upload files with an allowed file extension. '
            'Please try again to upload a file with the correct file'
            'extension.'))
    return True


checkphonenumber = re.compile(
    r'[+]{1}[0-9]{7}').match


def validatePhoneNumber(value):
    if not checkphonenumber(value):
        raise Invalid(_(
            safe_unicode('Invalid phone number')))
    return True
