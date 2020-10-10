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


def allowedconferencetalkslideextensions():
    return api.portal.get_registry_record('collectiveconference.allowed_talk_slide_extensions').replace('|', ', ')


def allowedconferencetalkmaterialextensions():
    return api.portal.get_registry_record('collectiveconference.allowed_talk_material_extension').replace('|', ', ')


def allowedconferenceworkshopslideextensions():
    return api.portal.get_registry_record('collectiveconference.allowed_workshop_slide_extensions').replace('|', ', ')


def allowedconferenceworkshopmaterialextensions():
    return api.portal.get_registry_record('collectiveconference.allowed_workshop_material_extension').replace('|', ', ')


def allowedconferencetrainingslideextensions():
    return api.portal.get_registry_record('collectiveconference.allowed_training_slide_extensions').replace('|', ', ')


def allowedconferencetrainingmaterialextensions():
    return api.portal.get_registry_record('collectiveconference.allowed_training_material_extension').replace('|', ', ')


def allowedconferencevideoextensions():
    return api.portal.get_registry_record('collectiveconference.allowed_video_file_extensions').replace('|', ', ')


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


def validatetalkslidefileextension(value):
    result = str(api.portal.get_registry_record('collectiveconference.allowed_talk_slide_extensions'))
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(safe_unicode(
            'You could only upload files with an allowed file extension. '
            'Please try again to upload a file with the correct file'
            'extension.'))
    return True


def validatelinkedtalkslidefileextension(value):
    result = str(api.portal.get_registry_record('collectiveconference.allowed_talk_slide_extensions'))
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value):
        raise Invalid(safe_unicode(
            'You could only link files with an allowed file extension. '
            'Please try again to link a file with the correct file'
            'extension.'))
    return True


def validatetalkmaterialfileextension(value):
    result = str(api.portal.get_registry_record('collectiveconference.allowed_talk_material_extension'))
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(safe_unicode(
            'You could only upload files with an allowed file extension. '
            'Please try again to upload a file with the correct file'
            'extension.'))
    return True


def validatelinkedtalkmaterialfileextension(value):
    result = str(api.portal.get_registry_record('collectiveconference.allowed_talk_material_extension'))
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value):
        raise Invalid(safe_unicode(
            'You could only link to files with an allowed file extension. '
            'Please try again with a link to a file with the correct file'
            'extension.'))
    return True


def validateworshopslidefileextension(value):
    result = str(api.portal.get_registry_record('collectiveconference.allowed_workshop_slide_extensions'))
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(safe_unicode(
            'You could only upload files with an allowed file extension. '
            'Please try again to upload a file with the correct file'
            'extension.'))
    return True


def validatelinkedworkshopslidefileextension(value):
    result = str(api.portal.get_registry_record('collectiveconference.allowed_workshop_slide_extensions'))
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value):
        raise Invalid(safe_unicode(
            'You could only link files with an allowed file extension. '
            'Please try again to link a file with the correct file'
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


def validatetrainingslidefileextension(value):
    result = str(api.portal.get_registry_record('collectiveconference.allowed_training_slide_extensions'))
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(safe_unicode(
            'You could only upload files with an allowed file extension. '
            'Please try again to upload a file with the correct file'
            'extension.'))
    return True


def validatelinkedtrainingslidefileextension(value):
    result = str(api.portal.get_registry_record('collectiveconference.allowed_training_slide_extensions'))
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value):
        raise Invalid(safe_unicode(
            'You could only link files with an allowed file extension. '
            'Please try again to link a file with the correct file'
            'extension.'))
    return True


def validatetrainingmaterialfileextension(value):
    result = str(api.portal.get_registry_record('collectiveconference.allowed_training_material_extension'))
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(safe_unicode(
            'You could only upload files with an allowed file extension. '
            'Please try again to upload a file with the correct file'
            'extension.'))
    return True


def validatevideofileextension(value):
    result = str(api.portal.get_registry_record('collectiveconference.allowed_video_file_extensions'))
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value):
        raise Invalid(safe_unicode(
            'You could only upload files with an allowed video file extension. '
            'Please try again to upload a file with the correct video file'
            'extension.'))
    return True


checkphonenumber = re.compile(
    r'[+]{1}[0-9]{7,}').match


def validatePhoneNumber(value):
    if not checkphonenumber(value):
        raise Invalid(_(
            safe_unicode('Invalid phone number')))
    return True


MULTISPACE = u'\u3000'


def quote_chars(value):
    # We need to quote parentheses when searching text indices
    if '(' in value:
        value = value.replace('(', '"("')
    if ')' in value:
        value = value.replace(')', '")"')
    if MULTISPACE in value:
        value = value.replace(MULTISPACE, ' ')
    return value
